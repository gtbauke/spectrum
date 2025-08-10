from celery import Celery
from eggp import EGGP
from reggression import Reggression
from datetime import datetime
from sqlmodel import Session, select

from app.utils.config import Config
from app.database import get_local_session
from app.resources.services.services import get_file_service
from app.resources.job_runs.models import JobRun, JobRunStatus

import pandas as pd

app = Celery("worker", broker=Config.REDIS_URL)


@app.task
def create_sr_model(file_path: str, job_run_id: str):
    session = get_local_session()
    file_service = get_file_service()

    job_run = session.get(JobRun, job_run_id)
    if not job_run:
        raise ValueError(f"JobRun with id {job_run_id} not found")

    if job_run.status != JobRunStatus.PENDING:
        raise ValueError(
            f"JobRun with id {job_run_id} is not in PENDING status")

    job_run.status = JobRunStatus.RUNNING
    session.add(job_run)
    session.commit()

    file_df = pd.read_csv(file_path, sep=",")

    dependent_variable_name = "target"
    independent_variable_names = [
        col for col in file_df.columns if col != dependent_variable_name
    ]

    X = file_df[independent_variable_names]
    y = file_df[dependent_variable_name].to_numpy()

    dump_to_file_path = file_service.get_file_path(
        f"{job_run.id}_{datetime.now().timestamp()}.eggp"
    )

    model = EGGP(dumpTo=str(dump_to_file_path))
    model.fit(X, y)

    egg = Reggression(
        dataset=job_run.job.dataset.dataset_file_path,
        loadFrom=str(dump_to_file_path),
    )

    job_run.status = JobRunStatus.COMPLETED
    job_run.finished_at = datetime.now()
    session.add(job_run)
    session.commit()

    top_models = egg.top(10)
    print(top_models)
