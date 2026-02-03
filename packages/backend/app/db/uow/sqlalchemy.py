from __future__ import annotations
from types import TracebackType
from typing import Callable, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.uow.unit_of_work import UnitOfWork
from app.repositories.sqlalchemy.datasets_repository import SqlAlchemyDatasetsRepository
from app.repositories.sqlalchemy.datasets_metadata_repository import SqlAlchemyDatasetsMetadataRepository


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session: Optional[AsyncSession] = None

    async def __aenter__(self) -> UnitOfWork:
        self._session = self._session_factory()

        self.datasets = SqlAlchemyDatasetsRepository(self._session)
        self.datasets_metadata = SqlAlchemyDatasetsMetadataRepository(
            self._session)

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
        else:
            await self.commit()

        await self._session.close()

    async def commit(self) -> None:
        assert self._session is not None
        await self._session.commit()

    async def rollback(self) -> None:
        assert self._session is not None
        await self._session.rollback()
