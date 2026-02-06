from uuid import UUID
from app.services.datasets.dataset_files_service import DatasetFilesService


class ModelFilesService:
    def __init__(
        self,
        dataset_files_service: DatasetFilesService
    ):
        self._dataset_files_service = dataset_files_service

    async def get_model_file_path(self, dataset_id: UUID, file_name: str) -> str:
        dataset_file_path = await self._dataset_files_service.get_dataset_file_path(
            dataset_id=dataset_id,
            file_name=file_name
        )

        return dataset_file_path.replace(".csv", "_model.eggp")
