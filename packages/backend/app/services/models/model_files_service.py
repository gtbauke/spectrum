from uuid import UUID
from pathlib import Path

from app.services.datasets.dataset_files_service import DatasetFilesService


class ModelFilesService:
    def __init__(
        self,
        dataset_files_service: DatasetFilesService
    ):
        self._dataset_files_service = dataset_files_service

    async def get_model_file_path(self, dataset_id: UUID, job_id: UUID) -> str:
        dataset_file_directory = await self._dataset_files_service.get_dataset_directory(dataset_id=dataset_id)
        model_file_name = f"{dataset_id}_{job_id}_model.eggp"

        return str(Path(dataset_file_directory) / model_file_name)
