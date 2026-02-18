from types import TracebackType
from typing import Callable, Optional, Type
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession

from core.ports.unit_of_work import UnitOfWork
from workers.repositories.outbox_repository import WorkerOutboxRepository


class WorkerUnitOfWork(UnitOfWork):
    outbox: WorkerOutboxRepository

    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self._session_factory = session_factory
        super().__init__()

    async def __aenter__(self):
        self.session = self._session_factory()
        self.outbox = WorkerOutboxRepository(self.session)

        return self

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def __aexit__(self, exc_type: Optional[Type[BaseException]],
                        exc: Optional[BaseException],
                        tb: Optional[TracebackType],):
        await self.session.close()

    async def get_outbox_repository(self, model_type: type[BaseModel]) -> WorkerOutboxRepository:
        return self.outbox
