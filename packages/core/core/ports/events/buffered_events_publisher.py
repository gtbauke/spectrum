import logging
from typing import Any

from core.ports.events.publisher import EventPublisher
from core.ports.events.message_broker import MessageBroker
from core.ports.transactional_resource import TransactionalResource

logger = logging.getLogger(__name__)


class BufferedEventsPublisher(EventPublisher, TransactionalResource):
    def __init__(self, broker: MessageBroker) -> None:
        super().__init__()

        self._broker = broker
        self._events_buffer: list[tuple[str, dict[str, Any]]] = []

    def publish(self, routing_key: str, payload: dict[str, Any]) -> None:
        self._events_buffer.append((routing_key, payload))

    async def commit(self) -> None:
        for routing_key, payload in self._events_buffer:
            logger.info(
                f"Publishing event: routing_key={routing_key} | payload={payload}")
            await self._broker.send(routing_key, payload)

        self._events_buffer.clear()

    async def rollback(self) -> None:
        self._events_buffer.clear()
