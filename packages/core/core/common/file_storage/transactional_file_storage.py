from __future__ import annotations
from abc import ABC, abstractmethod
from typing import BinaryIO


class TransactionalFileStorage(ABC):
    @abstractmethod
    async def stage(self, *, content: BinaryIO, destination: str) -> str:
        """
        Writes file to a temporary location.
        Returns the final logic path.
        """
        ...

    @abstractmethod
    async def commit(self) -> None:
        """
        Moves the file from the temporary location to the final location.
        Returns the final path.
        """
        ...

    @abstractmethod
    async def rollback(self) -> None:
        """
        Deletes the file from the temporary location.
        """
        ...
