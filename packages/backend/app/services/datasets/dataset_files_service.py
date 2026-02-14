import logging

from uuid import UUID
from fastapi import UploadFile
from datetime import datetime
from pathlib import Path

from app.infra.file_storage.base import FileStorage

logger = logging.getLogger(__name__)


class DatasetFilesService:
    def __init__(
        self,
        file_storage: FileStorage
    ):
        self._file_storage = file_storage

    async def get_dataset_directory(self, *, dataset_id: UUID) -> str:
        dataset_directory = await self._file_storage.get_full_path(file_path=str(dataset_id))
        Path(dataset_directory).mkdir(parents=True, exist_ok=True)

        return dataset_directory

    async def save_dataset_file(self, *, file: UploadFile, dataset_id: UUID):
        file_name = f"{datetime.now().timestamp()}_{file.filename}"
        final_path = await self.get_dataset_file_path(file_name=file_name, dataset_id=dataset_id)

        await self._file_storage.save(file=file, destination=str(final_path))
        return file_name

    async def get_dataset_file_path(self, file_name: str, dataset_id: UUID) -> str:
        dataset_directory = await self.get_dataset_directory(dataset_id=dataset_id)
        return str(Path(dataset_directory) / file_name)

    async def delete_dataset(self, *, dataset_id: UUID) -> None:
        dataset_directory = await self.get_dataset_directory(dataset_id=dataset_id)

        for file in Path(dataset_directory).glob("*"):
            await self._file_storage.delete(file_path=str(file))

        Path(dataset_directory).rmdir()
