from __future__ import annotations
from abc import ABC, abstractmethod
from typing import BinaryIO


class AbstractFileStorage(ABC):
    @abstractmethod
    async def save(self, *, content: BinaryIO, destination: str) -> str:
        """
        Save a file to the storage.

        Args:
            content (BinaryIO): The file content as a binary stream.
            destination (str): The destination path where the file should be saved.

        Returns:
            str: The full path to the saved file.
        """
        ...

    @abstractmethod
    async def delete(self, *, file_path: str) -> None:
        """
        Delete a file from the storage.

        Args:
            file_path (str): The path to the file that should be deleted.
        """
        ...

    @abstractmethod
    async def with_scope(self, scope: str) -> AbstractFileStorage:
        """
        Create a new instance of the file storage with a specific scope.

        Args:
            scope (str): The scope to be applied to the file storage.

        Returns:
            AbstractFileStorage: A new instance of the file storage with the specified scope.
        """
        ...
