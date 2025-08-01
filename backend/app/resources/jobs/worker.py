from celery import Celery
from eggp import EGGP

import pandas as pd

celery_app = Celery("worker", broker="redis://localhost:6379/0")


@celery_app.task
def process_file(file_path: str):
    # TODO: Implement file processing logic with EGGP
    pass
