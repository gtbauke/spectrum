from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Awaitable, Callable, Optional, Type, Literal, Union

from core.ports.transactional_resource import TransactionalResource

from core.ports.storage.file_storage import FileStorage

from core.repositories.auth import BaseAuthRepository
from core.repositories.users import BaseUsersRepository
from core.repositories.owners import BaseOwnersRepository
from core.repositories.datasets import (
    BaseDatasetsRepository,
    BaseDatasetVersionsRepository,
    BaseDatasetArtifactsRepository,
    BaseDatasetArtifactVersionsRepository,
)

from core.repositories.profiles import (
    BaseProfilesRepository,
    BaseProfileVersionsRepository,
    BaseProfileDatasetAssociationsRepository,
    BaseProfileBlocksRepository,
)

UnitOfWorkResources = Union[
    Literal["users"],
    Literal["auth"],
    Literal["owners"],
    Literal["datasets"],
    Literal["dataset_versions"],
    Literal["dataset_artifacts"],
    Literal["dataset_artifact_versions"],
    Literal["profiles"],
    Literal["profile_versions"],
    Literal["profile_dataset_associations"],
]


class UnitOfWork(ABC):
    users: BaseUsersRepository
    auth: BaseAuthRepository
    owners: BaseOwnersRepository
    datasets: BaseDatasetsRepository
    dataset_versions: BaseDatasetVersionsRepository
    dataset_artifacts: BaseDatasetArtifactsRepository
    dataset_artifact_versions: BaseDatasetArtifactVersionsRepository
    profiles: BaseProfilesRepository
    profile_versions: BaseProfileVersionsRepository
    profile_dataset_associations: BaseProfileDatasetAssociationsRepository
    profile_blocks: BaseProfileBlocksRepository

    file_storage: FileStorage

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
