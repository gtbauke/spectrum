from __future__ import annotations
from abc import ABC, abstractmethod
from types import TracebackType
from typing import Optional, Type

from app.repositories.datasets_repository import DatasetsRepository
from app.repositories.datasets_metadata_repository import DatasetsMetadataRepository
from app.repositories.models_repository import ModelsRepository
from app.repositories.jobs_repository import JobsRepository


class UnitOfWork(ABC):
    datasets: DatasetsRepository
    datasets_metadata: DatasetsMetadataRepository
    models: ModelsRepository
    jobs: JobsRepository

    @abstractmethod
    async def __aenter__(self) -> UnitOfWork: ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None: ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
