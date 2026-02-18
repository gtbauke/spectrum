from types import TracebackType
from typing import Callable, Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession


class WorkerUnitOfWork:
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self._session_factory = session_factory

    async def __aenter__(self):
        self.session = self._session_factory()

        # TODO: Initialize repositories here

        return self

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def __aexit__(self, exc_type: Optional[Type[BaseException]],
                        exc: Optional[BaseException],
                        tb: Optional[TracebackType],):
        await self.session.close()
