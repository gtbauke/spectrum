from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO


class StorageEngine(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_file_path(self, key: str) -> Path:
        pass

    @abstractmethod
    def save_file_obj(self, file_obj: BinaryIO, key: str) -> Path:
        pass

    @abstractmethod
    def save_file(self, file_path: Path, key: str) -> Path:
        pass
