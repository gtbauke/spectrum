import json
import logging

from typing import Any

import aio_pika
from aio_pika.abc import AbstractIncomingMessage, AbstractChannel

from core.ports.events.event_handler import EventHandler

logger = logging.getLogger(__name__)


class AioPikaConsumer:
    def __init__(
        self,
        *,
        channel: AbstractChannel,
        exchange_name: str,
        queue_name: str,
        handlers: list[EventHandler[Any]],
    ) -> None:
        self._channel = channel
        self._exchange_name = exchange_name
        self._queue_name = queue_name
        self._handlers: dict[str, EventHandler[Any]] = {
            handler.routing_key: handler for handler in handlers
        }

    async def start(self) -> None:
        exchange = await self._channel.declare_exchange(
            name=self._exchange_name,
            type=aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

        queue = await self._channel.declare_queue(
            name=self._queue_name,
            durable=True,
        )

        for routing_key in self._handlers:
            await queue.bind(
                exchange=exchange,
                routing_key=routing_key,
            )
            logger.info("Bound queue '%s' to routing key '%s'", self._queue_name, routing_key)

        await queue.consume(callback=self._on_message)
        logger.info("Consumer started, waiting for messages...")

    async def _on_message(self, message: AbstractIncomingMessage) -> None:
        routing_key = message.routing_key or ""

        handler = self._handlers.get(routing_key)
        if not handler:
            logger.warning("No handler registered for routing key '%s'", routing_key)
            await message.reject(requeue=False)
            return

        try:
            payload: dict[str, Any] = json.loads(message.body.decode("utf-8"))
            event = handler.parse(payload)
            await handler.handle(event=event)
            await message.ack()
            logger.info("Successfully handled message with routing key '%s'", routing_key)
        except Exception:
            logger.exception("Failed to handle message with routing key '%s'", routing_key)
            await message.nack(requeue=False)
