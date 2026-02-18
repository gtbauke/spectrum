import json

from abc import ABC
from aio_pika.abc import AbstractConnection, AbstractChannel
from aio_pika import Message
from pydantic import BaseModel


class EventMessage(Message):
    def __init__(self, event: str, payload: BaseModel, retry_count: int = 0):
        self._event = event
        self._payload = payload
        self._retry_count = retry_count

    def to_message(self) -> Message:
        return Message(
            body=json.dumps({
                "event": self._event,
                "payload": self._payload.model_dump(mode="json"),
            }).encode("utf-8"),
            headers={
                "x-retry-count": self._retry_count,
            },
        )


class EventPublisher(ABC):
    def __init__(
        self,
        connection: AbstractConnection,
        channel: AbstractChannel,
        exchange_id: str,
        routing_key: str,
    ):
        self._connection = connection
        self._channel = channel
        self._exchange_id = exchange_id
        self._routing_key = routing_key

    async def publish(self, message: EventMessage) -> None:
        exchange = await self._channel.get_exchange(self._exchange_id)
        message_to_send = message.to_message()

        await exchange.publish(
            message_to_send,
            routing_key=self._routing_key,
        )
