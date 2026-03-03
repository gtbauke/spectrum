from __future__ import annotations
from types import TracebackType
from typing import Callable, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.users.repository import UsersRepository
from core.ports.unit_of_work import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session: Optional[AsyncSession] = None
        super().__init__()

    async def __aenter__(self) -> UnitOfWork:
        self._session = self._session_factory()

        # TODO: initialize repositories
        self.users = UsersRepository(session=self._session)

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
