from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Awaitable, Callable, Optional, Type
from pydantic import BaseModel

from app.repositories.outbox_repository import OutboxRepository
from core.ports.transactional_resource import TransactionalResource
from core.repositories.datasets_repository import DatasetsRepository
from core.repositories.datasets_metadata_repository import DatasetsMetadataRepository
from core.repositories.jobs_repository import JobsRepository
from core.repositories.job_run_repository import JobRunRepository
from core.repositories.models_repository import ModelsRepository


class UnitOfWork(ABC):
    datasets: DatasetsRepository
    datasets_metadata: DatasetsMetadataRepository
    models: ModelsRepository
    jobs: JobsRepository
    job_runs: JobRunRepository
    outbox: OutboxRepository[BaseModel]

    def __init__(self) -> None:
        self._resources: list[TransactionalResource] = []
        self._on_commit_hooks: list[Callable[[], Awaitable[None]]] = []

    def register(self, resource: TransactionalResource) -> None:
        self._resources.append(resource)

    async def commit_resources(self) -> None:
        for resource in self._resources:
            await resource.commit()

        self._resources.clear()

    async def rollback_resources(self) -> None:
        for resource in self._resources:
            await resource.rollback()

        self._resources.clear()

    @abstractmethod
    async def __aenter__(self) -> UnitOfWork: ...

    @abstractmethod
    async def __aexit__(self, exc_type: Optional[Type[BaseException]],
                        exc: Optional[BaseException],
                        tb: Optional[TracebackType],): ...

    @abstractmethod
    async def commit(self) -> None: ...

    def on_commit(self, hook: Callable[[], Awaitable[None]]) -> None:
        self._on_commit_hooks.append(hook)

    @abstractmethod
    async def rollback(self) -> None: ...
