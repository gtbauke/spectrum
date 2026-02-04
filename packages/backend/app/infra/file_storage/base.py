from abc import ABC, abstractmethod

from pathlib import Path
from fastapi import UploadFile


class FileStorage(ABC):
    def __init__(self, base_path: str = "storage"):
        self._base_path = Path(base_path)

    @abstractmethod
    async def save(self, *, file: UploadFile, destination: str) -> str: ...

    @abstractmethod
    async def get_full_path(self, *, file_path: str) -> str: ...
