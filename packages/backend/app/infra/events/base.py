import json

from abc import ABC
from aio_pika.abc import AbstractConnection, AbstractChannel
from aio_pika import Message
from pydantic import BaseModel

from app.core.correlation import correlation_id_ctx


class EventMessage(Message):
    def __init__(self, event: str, payload: BaseModel):
        self._event = event
        self._payload = payload
        self._correlation_id = correlation_id_ctx.get()

    def to_message(self) -> Message:
        return Message(
            body=json.dumps({
                "event": self._event,
                "payload": self._payload.model_dump(mode="json"),
            }).encode("utf-8"),
            headers={"correlation_id": self._correlation_id},
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
