import json
import aio_pika

from typing import Any
from aio_pika.abc import AbstractExchange

from core.ports.events.message_broker import MessageBroker


class AioPikaBroker(MessageBroker):
    def __init__(self, exchange: AbstractExchange) -> None:
        self._exchange = exchange

    async def send(self, routing_key: str, payload: dict[str, Any]) -> None:
        message_body = json.dumps(payload).encode("utf-8")
        message = aio_pika.Message(
            body=message_body,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        await self._exchange.publish(message, routing_key=routing_key)
