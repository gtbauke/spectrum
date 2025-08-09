from celery import Celery
from eggp import EGGP

import pandas as pd

from app.resources.jobs.models import Job

celery_app = Celery("worker", broker="redis://localhost:6379/0")


@celery_app.task
def process_file(file_path: str, job: Job):
    file_df = pd.read_csv(file_path, sep=",")

    dependent_variable_name = "target"
    independent_variable_names = [
        col for col in file_df.columns if col != dependent_variable_name]

    X = file_df[independent_variable_names]
    y = file_df[dependent_variable_name].to_numpy()

    model = EGGP(
        gen=job.generations,
        nPop=job.population_size,
        maxSize=job.max_expression_size,
        nTournament=job.tournament_size,
        pc=job.crossover_probability,
        pm=job.mutation_probability,
        loss=job.loss_function,
        optIter=job.max_optimization_iterations,
        optRepeat=job.max_optimization_restarts,
        nParams=job.parameter_count,
        simplify=job.simplify,
        dumpTo="C:/users/gusta/dev/spectrum/examples/dump.eggp",
        loadFrom="C:/users/gusta/dev/spectrum/examples/dump.eggp"
    )

    model.fit(X, y)
