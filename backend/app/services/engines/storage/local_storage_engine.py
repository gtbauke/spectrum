import os
import aiofiles

from pathlib import Path
from typing import BinaryIO
from .storage_engine import StorageEngine


class LocalStorageEngine(StorageEngine):
    LOCAL_FILES_PATH = Path(os.path.curdir) / "spectrum_files"
    CHUNK_SIZE = 1024

    def __init__(self, local_path: str | None = None):
        super().__init__()
        self.base_dir = self.LOCAL_FILES_PATH / \
            local_path if local_path is not None else self.LOCAL_FILES_PATH

    async def get_file_path(self, key: str) -> Path:
        return self.base_dir / key

    async def save_file_obj(self, file_obj: BinaryIO, key: str) -> Path:
        os.makedirs(self.base_dir, exist_ok=True)
        file_path = self.base_dir / key

        async with aiofiles.open(file_path, "wb") as out_file:
            while chunk := file_obj.read(self.CHUNK_SIZE * self.CHUNK_SIZE):
                await out_file.write(chunk)

        return file_path

    async def delete(self, key: str) -> None:
        file_path = self.base_dir / key
        if os.path.exists(file_path):
            os.remove(file_path)
