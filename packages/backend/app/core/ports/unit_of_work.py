from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import TYPE_CHECKING, Awaitable, Callable, Optional, Type

from app.core.ports.transactional_resource import TransactionalResource
from app.core.ports.storage.file_storage import FileStorage
from app.core.ports.events.publisher import EventPublisher

if TYPE_CHECKING:
    from app.features.users.repository import IUsersRepository
    from app.features.auth.repository import IAuthRepository
    from app.features.datasets.repository import IDatasetsRepository, IArtifactsRepository
    from app.features.profiles.blocks.repository import IBlocksRepository
    from app.features.profiles.jobs.repository import IJobsRepository
    from app.features.profiles.models.repository import IModelsRepository
    from app.features.profiles.jobs.runs.repository import IRunsRepository
    from app.features.profiles.repository import IProfilesRepository
    from app.features.profiles.blocks.inference.repository import IInferenceRunRepository, IInferenceResultRepository


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
    inference_runs: IInferenceRunRepository
    inference_results: IInferenceResultRepository

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
