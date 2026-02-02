from abc import ABC, abstractmethod
from aio_pika.abc import AbstractConnection, AbstractChannel
from pydantic import BaseModel


class EventPublisher(ABC):
    def __init__(self, connection: AbstractConnection, channel: AbstractChannel):
        self._connection = connection
        self._channel = channel

    @abstractmethod
    async def publish(self, event: str, payload: BaseModel) -> None: ...
