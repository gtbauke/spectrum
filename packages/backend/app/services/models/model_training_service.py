import pandas as pd

from uuid import UUID
from pathlib import Path
from eggp import EGGP  # type: ignore

from app.services.models.model_files_service import ModelFilesService
from app.services.datasets.dataset_files_service import DatasetFilesService


class ModelTrainingService:
    def __init__(
        self,
        dataset_files_service: DatasetFilesService,
        model_files_service: ModelFilesService
    ):
        self._dataset_files_service = dataset_files_service
        self._model_files_service = model_files_service

    async def train_model(self, dataset_id: UUID, dataset_file_name: str) -> str:
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
            file_name=dataset_file_name
        )

        model_path = Path(model_path)
        model_path.touch(exist_ok=True)

        model = EGGP(dumpTo=str(model_path))
        model.fit(X, y)  # type: ignore

        print(f"Model trained and saved to {model_path}")

        return dataset_file_name.replace(".csv", "_model.eggp")
