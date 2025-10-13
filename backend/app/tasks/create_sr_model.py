from celery import Celery
from eggp import EGGP
from datetime import datetime

from app.utils.config import Config
from app.database import get_local_session
from app.services import get_file_service
from app.resources.job_runs.models import JobRun, JobRunStatus

import pandas as pd

app = Celery("worker", broker=Config.REDIS_URL)


@app.task
def create_sr_model(file_path: str, job_run_id: str):
    print("RUNNING MODEL")
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

    try:
        file_df = pd.read_csv(file_path, sep=",")
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

    dump_to_file_path = file_service.get_file_path(
        f"{job_run.id}_{datetime.now().timestamp()}.eggp"
    )

    model = EGGP(dumpTo=str(dump_to_file_path))
    model.fit(X, y)

    job_run.status = JobRunStatus.COMPLETED
    job_run.finished_at = datetime.now()
    job_run.eggp_file_path = str(dump_to_file_path)

    session.add(job_run)
    session.commit()
