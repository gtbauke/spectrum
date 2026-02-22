from abc import ABC, abstractmethod
from types import TracebackType
from typing import Optional, Type

from pydantic import BaseModel
from db.session import AsyncSessionLocal

from workers.common.get_uow import WorkerUnitOfWork
from workers.infra.rabbitmq.setup import setup_all
from workers.infra.rabbitmq.session import create_connection


class AbstractConsumer[Event: BaseModel](ABC):
    async def __aenter__(self):
        self._connection, self._channel = await create_connection()
        await setup_all(self._channel)

        self._unit_of_work = WorkerUnitOfWork(AsyncSessionLocal)
        self.uow = await self._unit_of_work.__aenter__()

        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]],
                        exc: Optional[BaseException],
                        tb: Optional[TracebackType],):
        await self._unit_of_work.__aexit__(exc_type, exc, tb)

        await self._channel.close()
        await self._connection.close()

    @property
    def outbox(self):
        return self.uow.outbox

    @abstractmethod
    async def consume(self, event: Event): ...
