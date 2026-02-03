import aiofiles

from pathlib import Path
from uuid import UUID
from fastapi import UploadFile

from app.infra.file_storage.base import FileStorage
from app.core.config import settings


class LocalFileStorage(FileStorage):
    def __init__(self, base_path: str = "storage"):
        self.base_path = Path(base_path)

    async def save(self, *, file: UploadFile, destination: str) -> str:
        dataset_dir = settings.FILE_STORAGE_ROOT_PATH / self.base_path / destination
        dataset_dir.mkdir(parents=True, exist_ok=True)

        file_name = file.filename if file.filename else str(UUID())
        file_path = dataset_dir / file_name

        async with aiofiles.open(file_path, 'wb') as out_file:
            while chunk := await file.read(1024):
                await out_file.write(chunk)

        await file.close()
        return str(file_path)

    async def get_full_path(self, *, file_path: str) -> str:
        path = Path(settings.FILE_STORAGE_ROOT_PATH) / file_path
        return str(path)
