from celery import Celery
from eggp import EGGP
from reggression import Reggression
from datetime import datetime
from os import getenv

import pandas as pd

from app.resources.services.file_service import FileService
from app.resources.job_runs.models import JobRun

REDIS_URL = getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("worker", broker=REDIS_URL)


@celery_app.task
def process_file(file_path: str, job_run: JobRun, file_service: FileService):
    file_df = pd.read_csv(file_path, sep=",")

    dependent_variable_name = "target"
    independent_variable_names = [
        col for col in file_df.columns if col != dependent_variable_name]

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

    top_models = egg.top(10)
    print(top_models)
