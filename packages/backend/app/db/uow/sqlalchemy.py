from __future__ import annotations
from types import TracebackType
from typing import Callable, Optional
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.outbox_repository import OutboxRepository, SqlAlchemyOutboxRepository
from core.ports.unit_of_work import UnitOfWork

from app.repositories.datasets_repository import SqlAlchemyDatasetsRepository
from app.repositories.datasets_metadata_repository import SqlAlchemyDatasetsMetadataRepository
from app.repositories.models_repository import SqlAlchemyModelsRepository
from app.repositories.jobs_repository import SQLAlchemyJobsRepository
from app.repositories.job_run_repository import SQLAlchemyJobRunRepository


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session: Optional[AsyncSession] = None
        super().__init__()

    async def __aenter__(self) -> UnitOfWork:
        self._session = self._session_factory()

        self.datasets = SqlAlchemyDatasetsRepository(self._session)
        self.datasets_metadata = SqlAlchemyDatasetsMetadataRepository(
            self._session)

        self.models = SqlAlchemyModelsRepository(self._session)
        self.jobs = SQLAlchemyJobsRepository(self._session)

        self.job_runs = SQLAlchemyJobRunRepository(self._session)

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

    async def get_outbox_repository[T: BaseModel](self, model_type: type[T]) -> OutboxRepository[T]:
        assert self._session is not None

        return SqlAlchemyOutboxRepository[T](self._session, model_type)
