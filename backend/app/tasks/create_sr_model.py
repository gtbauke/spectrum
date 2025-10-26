import asyncio
import os
import shutil
import requests
import tempfile

from pathlib import Path
from app.integrations.aws.session import Boto3SessionOptions
from app.services.file_service import FileService
from celery import Celery
from celery.utils.log import get_task_logger
from eggp import EGGP
from datetime import datetime
from botocore.exceptions import ClientError

from app.utils.config import Config
from app.database import get_local_session
from app.resources.datasets.models import Dataset  # type: ignore
from app.resources.jobs.models import Job  # type: ignore
from app.resources.job_runs.models import JobRun, JobRunStatus
from . import celery_config

import pandas as pd

app = Celery("worker", broker=Config.REDIS_URL)
app.config_from_object(celery_config)

logger = get_task_logger(__name__)


@app.task
def create_sr_model_task(file_path: str, job_run_id: str):
    logger.info(f"AWS_ACCESS_KEY: {app.conf.AWS_ACCESS_KEY}")
    logger.info(f"AWS_SECRET_KEY: {app.conf.AWS_SECRET_KEY}")
    logger.info(f"FILE_SERVICE_TYPE: {app.conf.FILE_SERVICE_TYPE}")

    session = get_local_session()
    file_service = FileService(temp_engine_base_dir="spectrum_datasets", options=Boto3SessionOptions(
        region_name=app.conf.REGION_NAME,
        aws_access_key_id=app.conf.AWS_ACCESS_KEY,
        aws_secret_access_key=app.conf.AWS_SECRET_KEY,
    ))

    job_run = session.get(JobRun, job_run_id)
    if not job_run:
        raise ValueError(f"JobRun with id {job_run_id} not found")

    if job_run.status != JobRunStatus.PENDING:
        raise ValueError(
            f"JobRun with id {job_run_id} is not in PENDING status")

    job_run.status = JobRunStatus.RUNNING
    session.add(job_run)
    session.commit()

    file_to_delete = None
    try:
        file_name = file_service.remote_engine.get_presigned_url(
            file_path.split(".com/")[-1]) if "https" in file_path else file_path

        local_file_path = file_path
        if "http" in file_name:
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_path = temp_file.name
            temp_file.close()

            with requests.get(file_name, stream=True) as r:
                r.raise_for_status()
                with open(temp_path, "wb") as f:
                    shutil.copyfileobj(r.raw, f)

            local_file_path = temp_path
            file_to_delete = temp_path

        logger.warning(f"Reading local file {local_file_path}")
        file_df = pd.read_csv(local_file_path, sep=",")  # type: ignore
    except (FileNotFoundError, ClientError) as e:
        logger.info("JOB RUN FAILED")
        logger.info(e)

        job_run.status = JobRunStatus.FAILED
        job_run.finished_at = datetime.now()

        session.add(job_run)
        session.commit()

        return

    dependent_variable_name = "target"
    independent_variable_names = [
        col for col in file_df.columns if col != dependent_variable_name
    ]

    X = file_df[independent_variable_names]
    y = file_df[dependent_variable_name].to_numpy()

    eggp_file_name = f"{job_run.id}_{datetime.now().timestamp()}.eggp"

    temp_file_folder = Path(tempfile.gettempdir(
    )) / "spectrum_datasets" / str(job_run.job.dataset_id) / str(job_run.job_id)
    temp_file_folder.mkdir(parents=True, exist_ok=True)

    path = temp_file_folder / eggp_file_name
    path.touch(exist_ok=True)

    logger.warning(f"Saving eggp file to {path}")

    model = EGGP(dumpTo=str(path))
    model.fit(X, y)  # type: ignore

    with open(path, "rb") as f:
        key = str(Path(str(job_run.job.dataset_id)) /
                  str(job_run.job_id) / eggp_file_name)

        asyncio.run(file_service.remote_engine.save_file_obj(f, key))

    job_run.status = JobRunStatus.COMPLETED
    job_run.finished_at = datetime.now()
    job_run.eggp_file_path = str(
        Path(str(job_run.job.dataset_id)) / str(job_run.job_id) / eggp_file_name)

    session.add(job_run)
    session.commit()

    if file_to_delete is not None:
        os.remove(file_to_delete)

    logger.info("Task completed: model successfully trained")
