import pandas as pd

from uuid import UUID
from pathlib import Path
from eggp import EGGP  # type: ignore

from app.api.deps import UnitOfWork
from app.services.models.model_files_service import ModelFilesService
from app.services.datasets.dataset_files_service import DatasetFilesService
from app.services.jobs.jobs_service import JobsService
from app.domain.jobs.available_functions import AvailableFunctions


class ModelTrainingService:
    def __init__(
        self,
        dataset_files_service: DatasetFilesService,
        model_files_service: ModelFilesService,
        jobs_service: JobsService,
    ):
        self._dataset_files_service = dataset_files_service
        self._model_files_service = model_files_service
        self._jobs_service = jobs_service

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

        print(f"Model trained and saved to {model_path}")

        return dataset_file_name.replace(".csv", "_model.eggp")
