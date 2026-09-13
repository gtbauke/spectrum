import asyncio
import json
import logging

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractIncomingMessage

logger = logging.getLogger(__name__)

CONTROL_EXCHANGE = "spectrum.control"


class ControlListener:
    """Listens on a per-worker control queue for management commands.

    Currently supported commands:
    - ``restart`` — sets a flag that the main loop can check to
      gracefully tear down and restart consumers.
    """

    def __init__(
        self,
        *,
        channel: AbstractChannel,
        worker_id: str,
    ) -> None:
        self._channel = channel
        self._worker_id = worker_id
        self._restart_event = asyncio.Event()

    @property
    def restart_requested(self) -> bool:
        return self._restart_event.is_set()

    def get_restart_event(self) -> asyncio.Event:
        return self._restart_event

    async def start(self) -> None:
        """Declare a per-worker control queue and begin consuming."""
        exchange = await self._channel.declare_exchange(
            name=CONTROL_EXCHANGE,
            type=aio_pika.ExchangeType.DIRECT,
            durable=True,
        )

        # Exclusive, auto-delete queue — disappears when the worker disconnects
        queue = await self._channel.declare_queue(
            name=f"control.{self._worker_id}",
            auto_delete=True,
        )

        routing_key = f"control.{self._worker_id}"
        await queue.bind(exchange=exchange, routing_key=routing_key)

        await queue.consume(callback=self._on_message)
        logger.info(
            "Control listener started for '%s' (routing_key=%s)",
            self._worker_id, routing_key,
        )

    async def _on_message(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            try:
                body = json.loads(message.body.decode("utf-8"))
                command = body.get("command", "")
                logger.info("Received control command: %s", command)

                if command == "restart":
                    logger.info("Restart requested for worker '%s'", self._worker_id)
                    self._restart_event.set()
                else:
                    logger.warning("Unknown control command: %s", command)
            except Exception:
                logger.exception("Failed to process control message")
