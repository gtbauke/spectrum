from pathlib import Path
from fastapi import UploadFile
from datetime import datetime

from app.infra.file_storage.base import FileStorage


class DatasetFilesService:
    def __init__(self, file_storage: FileStorage):
        self._file_storage = file_storage

    async def save_dataset_file(self, *, file: UploadFile):
        file_name = file.filename if file.filename else f"file_{datetime.now().timestamp()}"
        final_path = await self.get_dataset_file_path(file_name=file_name)

        await self._file_storage.save(file=file, destination=str(final_path))
        return file_name

    async def get_dataset_file_path(self, file_name: str) -> str:
        with_datasets_folder = Path("datasets") / file_name
        full_path = await self._file_storage.get_full_path(file_path=str(with_datasets_folder))

        return str(full_path)
