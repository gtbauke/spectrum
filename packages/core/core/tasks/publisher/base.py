import json

from aio_pika import Message
from aio_pika.abc import AbstractChannel
from abc import ABC

from core.tasks.base import AbstractTaskEvent


class AbstractTaskPublisher(ABC):
    def __init__(self, channel: AbstractChannel):
        self._channel = channel

    async def publish(self, event: AbstractTaskEvent):
        await self._channel.default_exchange.publish(
            routing_key=event.task_type,
            message=Message(
                body=json.dumps(event.model_dump(mode="json")).encode("utf-8"),
            )
        )
