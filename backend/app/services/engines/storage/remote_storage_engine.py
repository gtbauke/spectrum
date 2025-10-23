from pathlib import Path
from typing import BinaryIO
from storage_engine import StorageEngine


class RemoteStorageEngine(StorageEngine):
    def get_file_path(self, key: str) -> Path:
        return super().get_file_path(key)

    def save_file_obj(self, file_obj: BinaryIO, key: str) -> Path:
        return super().save_file_obj(file_obj, key)

    def save_file(self, file_path: Path, key: str) -> Path:
        return super().save_file(file_path, key)
