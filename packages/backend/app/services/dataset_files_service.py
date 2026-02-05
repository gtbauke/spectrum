import logging
from uuid import UUID
from fastapi import UploadFile
from datetime import datetime

from app.infra.file_storage.base import FileStorage

logger = logging.getLogger(__name__)


# TODO: fix file saving and retrieval logic
class DatasetFilesService:
    def __init__(self, file_storage: FileStorage):
        self._file_storage = file_storage

    async def save_dataset_file(self, *, file: UploadFile, dataset_id: UUID):
        file_name = file.filename if file.filename else f"file_{datetime.now().timestamp()}"
        final_path = await self.get_dataset_file_path(file_name=file_name, dataset_id=dataset_id)

        await self._file_storage.save(file=file, destination=str(final_path))
        return final_path

    async def get_dataset_file_path(self, file_name: str, dataset_id: UUID) -> str:
        full_path = await self._file_storage.get_full_path(file_path=f"{dataset_id}/{file_name}")
        logger.info("get_dataset_file_path", extra={
                    "file_name": file_name, "full_path": full_path})

        return str(full_path)
