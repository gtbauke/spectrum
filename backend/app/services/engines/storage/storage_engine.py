from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO


class StorageEngine(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def get_file_path(self, key: str) -> Path | str:
        pass

    @abstractmethod
    async def save_file_obj(self, file_obj: BinaryIO, key: str) -> Path | str:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass
