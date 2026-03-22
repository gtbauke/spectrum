from __future__ import annotations

from types import TracebackType
from typing import Callable, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from db.features.users.repository import SqlAlchemyUsersRepository
from db.features.auth.repository import SqlAlchemyAuthRepository
from db.features.datasets.repository import SqlAlchemyDatasetsRepository, SqlAlchemyArtifactsRepository
from db.features.profiles.repository import SqlAlchemyProfilesRepository
from db.features.profiles.blocks.repository import SqlAlchemyBlocksRepository
from db.features.profiles.jobs.repository import SqlAlchemyJobsRepository
from db.features.profiles.jobs.runs.repository import SqlAlchemyRunsRepository
from db.features.profiles.models.repository import SqlAlchemyModelsRepository

from core.ports.events.message_broker import MessageBroker
from core.ports.unit_of_work import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession], broker: MessageBroker) -> None:
        self._session_factory = session_factory
        self._session: Optional[AsyncSession] = None
        self._broker = broker

        super().__init__()

    async def __aenter__(self) -> UnitOfWork:
        self._session = self._session_factory()

        self.users = SqlAlchemyUsersRepository(self._session)
        self.auth = SqlAlchemyAuthRepository(self._session)
        self.datasets = SqlAlchemyDatasetsRepository(self._session)
        self.artifacts = SqlAlchemyArtifactsRepository(self._session)
        self.profiles = SqlAlchemyProfilesRepository(self._session)
        self.blocks = SqlAlchemyBlocksRepository(self._session)
        self.jobs = SqlAlchemyJobsRepository(self._session)
        self.runs = SqlAlchemyRunsRepository(self._session)
        self.models = SqlAlchemyModelsRepository(self._session)

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
