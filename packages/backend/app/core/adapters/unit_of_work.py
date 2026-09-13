from __future__ import annotations

from pathlib import Path
from types import TracebackType
from typing import Callable, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.ports.events.message_broker import MessageBroker
from app.core.ports.unit_of_work import UnitOfWork
from app.core.adapters.storage.local_storage import LocalStorage
from app.core.adapters.storage.s3_storage import S3FileStorage
from app.core.adapters.events.buffered_events_publisher import BufferedEventsPublisher

from app.features.users.repository import SqlAlchemyUsersRepository
from app.features.auth.repository import SqlAlchemyAuthRepository
from app.features.datasets.repository import (
    SqlAlchemyDatasetsRepository,
    SqlAlchemyArtifactsRepository,
)
from app.features.profiles.repository import SqlAlchemyProfilesRepository
from app.features.profiles.blocks.repository import SqlAlchemyBlocksRepository
from app.features.profiles.jobs.repository import SqlAlchemyJobsRepository
from app.features.profiles.jobs.runs.repository import SqlAlchemyRunsRepository
from app.features.profiles.models.repository import SqlAlchemyModelsRepository
from app.features.profiles.blocks.inference.repository import (
    SqlAlchemyInferenceRunRepository,
    SqlAlchemyInferenceResultRepository,
)


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(
        self,
        session_factory: Callable[[], AsyncSession],
        broker: MessageBroker,
    ) -> None:
        super().__init__()
        self._session_factory = session_factory
        self._session: Optional[AsyncSession] = None
        self._broker = broker

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
        self.inference_runs = SqlAlchemyInferenceRunRepository(self._session)
        self.inference_results = SqlAlchemyInferenceResultRepository(
            self._session)

        if settings.STORAGE_TYPE == "s3":
            self.file_storage = S3FileStorage(
                bucket=settings.S3_BUCKET,
                region=settings.S3_REGION,
                access_key=settings.S3_ACCESS_KEY,
                secret_key=settings.S3_SECRET_KEY,
                endpoint_url=settings.S3_ENDPOINT_URL,
            )
        else:
            self.file_storage = LocalStorage(
                base_path=Path(settings.FILE_STORAGE_SPECTRUM_DATA_PATH),
                base_url=settings.STORAGE_BASE_URL,
            )

        self.events_publisher = BufferedEventsPublisher(self._broker)
        self.register(self.events_publisher)

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


# Alias for backward compatibility in worker handlers
WorkerUnitOfWork = SqlAlchemyUnitOfWork
