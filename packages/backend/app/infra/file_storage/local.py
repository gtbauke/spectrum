import logging
import aiofiles

from fastapi import UploadFile
from pathlib import Path

from app.infra.file_storage.base import FileStorage
from app.core.config import settings


logger = logging.getLogger(__name__)


class LocalFileStorage(FileStorage):
    async def save(self, *, file: UploadFile, destination: str) -> str:
        parent_folder = Path(destination).parent
        parent_folder.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(destination, 'wb') as out_file:
            while chunk := await file.read(1024):
                await out_file.write(chunk)

        await file.close()
        return str(destination)

    async def get_full_path(self, *, file_path: str) -> str:
        logger.info("get_full_path", extra={
            "file_path": file_path,
            "root_path": settings.FILE_STORAGE_ROOT_PATH,
            "base_path": self._base_path,
        })

        full_path = settings.FILE_STORAGE_ROOT_PATH / self._base_path / file_path
        return str(full_path)
