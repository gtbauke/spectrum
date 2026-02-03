from abc import ABC, abstractmethod

from fastapi import UploadFile


class FileStorage(ABC):
    @abstractmethod
    async def save(self, *, file: UploadFile, destination: str) -> str: ...

    @abstractmethod
    async def get_full_path(self, *, file_path: str) -> str: ...
