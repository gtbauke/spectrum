from pathlib import Path
import tempfile
from celery import Celery
from eggp import EGGP
from datetime import datetime

from app.utils.config import Config
from app.database import get_local_session
from app.services import get_file_service
from app.resources.job_runs.models import JobRun, JobRunStatus
from . import celery_config

import pandas as pd

app = Celery("worker", broker=Config.REDIS_URL)
app.config_from_object(celery_config)


@app.task
def create_sr_model(file_path: str, job_run_id: str):
    print("RUNNING MODEL")
    print(f"AWS_ACCESS_KEY: {app.conf.AWS_ACCESS_KEY}")
    print(f"AWS_SECRET_KEY: {app.conf.AWS_SECRET_KEY}")
    session = get_local_session()
    file_service = get_file_service(override="s3", options={
        "aws_access_key_id": app.conf.AWS_ACCESS_KEY,
        "aws_secret_access_key": app.conf.AWS_SECRET_KEY
    })

    job_run = session.get(JobRun, job_run_id)
    if not job_run:
        raise ValueError(f"JobRun with id {job_run_id} not found")

    if job_run.status != JobRunStatus.PENDING:
        raise ValueError(
            f"JobRun with id {job_run_id} is not in PENDING status")

    job_run.status = JobRunStatus.RUNNING
    session.add(job_run)
    session.commit()

    try:
        file_name = f"s3://{Config.S3_BUCKET_NAME}/{file_path.split(".com/")[-1]}" if "http" in file_path else file_path
        print(f"READING FROM {file_name}")

        file_df = pd.read_csv(file_name, sep=",")
    except FileNotFoundError:
        print("JOB RUN FAILED")

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
    dump_to_file_path = f"{job_run.job.dataset_id}/{job_run.job_id}/{eggp_file_name}"

    TEMP_FILE_DIR = Path(tempfile.gettempdir()) / "spectrum_datasets"
    TEMP_FILE_DIR.mkdir(parents=True, exist_ok=True)
    path = TEMP_FILE_DIR / eggp_file_name

    model = EGGP(dumpTo=str(path))
    model.fit(X, y)

    file_service.upload_file_from_path(
        str(path), str(dump_to_file_path))

    job_run.status = JobRunStatus.COMPLETED
    job_run.finished_at = datetime.now()
    job_run.eggp_file_path = dump_to_file_path

    session.add(job_run)
    session.commit()
