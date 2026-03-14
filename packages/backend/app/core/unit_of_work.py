from __future__ import annotations

from types import TracebackType
from typing import Callable, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.repository import AuthRepository
from app.features.users.repository import UsersRepository
from app.features.owners.repository import OwnersRepository
from app.features.datasets.repository import DatasetsRepository
from app.features.datasets.versions.repository import DatasetVersionsRepository
from app.features.datasets.artifacts.repository import DatasetArtifactsRepository
from app.features.datasets.artifact_version.repository import DatasetArtifactVersionsRepository
from app.features.profiles.repository import ProfilesRepository
from app.features.profiles.versions.repository import ProfileVersionsRepository
from app.features.profiles.associations.repository import ProfileDatasetAssociationsRepository
from app.features.profiles.blocks.repository import ProfileBlocksRepository

from app.adapters.storage.local_storage import LocalStorage

from core.ports.unit_of_work import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session: Optional[AsyncSession] = None
        super().__init__()

    async def __aenter__(self) -> UnitOfWork:
        self._session = self._session_factory()

        self.users = UsersRepository(session=self._session)
        self.auth = AuthRepository(session=self._session)
        self.owners = OwnersRepository(session=self._session)
        self.datasets = DatasetsRepository(session=self._session)
        self.dataset_versions = DatasetVersionsRepository(
            session=self._session)
        self.dataset_artifacts = DatasetArtifactsRepository(
            session=self._session)
        self.dataset_artifact_versions = DatasetArtifactVersionsRepository(
            session=self._session)

        self.profiles = ProfilesRepository(session=self._session)
        self.profile_versions = ProfileVersionsRepository(
            session=self._session)
        self.profile_dataset_associations = ProfileDatasetAssociationsRepository(
            session=self._session)
        self.profile_blocks = ProfileBlocksRepository(
            session=self._session
        )

        self.file_storage = LocalStorage()

        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        assert self._session is not None

        if exc:
            await self.rollback()
            return

        try:
            await self.commit()

            for hook in self._on_commit_hooks:
                await hook()
        except Exception:
            await self.rollback()
            raise
        finally:
            await self._session.close()
            self._on_commit_hooks.clear()

    async def commit(self) -> None:
        assert self._session is not None

        await self._session.commit()
        await self.commit_resources()

    async def rollback(self) -> None:
        assert self._session is not None

        await self._session.rollback()
        await self.rollback_resources()

    async def flush(self) -> None:
        assert self._session is not None

        await self._session.flush()
