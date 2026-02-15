import logging
import pandas as pd

from uuid import UUID
from pathlib import Path
from eggp import EGGP  # type: ignore

from app.api.deps import UnitOfWork
from app.services.models.model_files_service import ModelFilesService
from app.services.datasets.dataset_files_service import DatasetFilesService
from app.services.jobs.jobs_service import JobsService
from app.services.models.models_service import ModelsService
from app.domain.jobs.available_functions import AvailableFunctions
from app.domain.jobs.job_status import JobStatus


logger = logging.getLogger(__name__)


class ModelTrainingService:
    def __init__(
        self,
        dataset_files_service: DatasetFilesService,
        model_files_service: ModelFilesService,
        jobs_service: JobsService,
        models_service: ModelsService,
    ):
        self._dataset_files_service = dataset_files_service
        self._model_files_service = model_files_service
        self._jobs_service = jobs_service
        self._models_service = models_service

    async def can_train_model(
        self,
        *,
        uow: UnitOfWork,
        model_id: UUID,
    ):
        async with uow:
            model = await self._models_service.get(uow=uow, model_id=model_id)

            if not model:
                raise ValueError(f"Model with ID {model_id} not found.")

            if not model.job:
                raise ValueError(
                    f"Model with ID {model_id} has no associated job.")

            if model.job.status == JobStatus.RUNNING:
                return None

        return model

    async def train_model(
        self,
        *,
        uow: UnitOfWork,
        dataset_id: UUID,
        job_id: UUID,
        dataset_file_name: str
    ) -> str:
        file_path = await self._dataset_files_service.get_dataset_file_path(
            dataset_id=dataset_id,
            file_name=dataset_file_name
        )

        data = pd.read_csv(file_path)  # type: ignore

        independent_variables = [
            col for col in data.columns if col != "target"
        ]

        X = data[independent_variables]
        y = data["target"]

        model_path = await self._model_files_service.get_model_file_path(
            dataset_id=dataset_id,
            job_id=job_id,
        )

        model_path = Path(model_path)
        model_path.touch(exist_ok=True)

        async with uow:
            job = await self._jobs_service.get_by_id(uow=uow, job_id=job_id)

            if not job:
                raise ValueError(f"Job with id {job_id} not found")

        logger.info("Non-terminals for job %s: %s", job_id, job.non_terminals, extra={
            "job_id": job_id,
            "non_terminals": job.non_terminals,
            "non_terminals_str": AvailableFunctions.from_list(*job.non_terminals)
        })

        model = EGGP(
            gen=job.generations,
            nPop=job.population,
            maxSize=job.max_size,
            nTournament=job.number_of_tournaments,
            pc=job.crossover_probability,
            pm=job.mutation_probability,
            nonterminals=AvailableFunctions.from_list(*job.non_terminals),
            loss=job.loss,
            optIter=job.optimization_iterations,
            optRepeat=job.optimization_repeats,
            nParams=job.max_param_count,
            simplify=job.simplify,
            dumpTo=str(model_path)
        )

        model.fit(X, y)  # type: ignore
        return dataset_file_name.replace(".csv", "_model.eggp")
