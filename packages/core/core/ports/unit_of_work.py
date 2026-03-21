from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Awaitable, Callable, Optional, Type, Literal, Union

from core.ports.transactional_resource import TransactionalResource
from core.ports.storage.file_storage import FileStorage
from core.ports.events.publisher import EventPublisher

from core.features.users.repository import IUsersRepository
from core.features.auth.repository import IAuthRepository
from core.features.datasets.repository import IDatasetsRepository, IArtifactsRepository
from core.features.profiles.blocks.repository import IBlocksRepository
from core.features.profiles.jobs.repository import IJobsRepository
from core.features.profiles.models.repository import IModelsRepository
from core.features.profiles.jobs.runs.repository import IRunsRepository
from core.features.profiles.repository import IProfilesRepository


class UnitOfWork(ABC):
    users: IUsersRepository
    auth: IAuthRepository
    datasets: IDatasetsRepository
    artifacts: IArtifactsRepository
    profiles: IProfilesRepository
    blocks: IBlocksRepository
    jobs: IJobsRepository
    models: IModelsRepository
    runs: IRunsRepository

    file_storage: FileStorage
    events_publisher: EventPublisher

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
