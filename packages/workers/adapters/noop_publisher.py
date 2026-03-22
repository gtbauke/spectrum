from typing import Any

from core.ports.events.publisher import EventPublisher
from core.ports.transactional_resource import TransactionalResource


class NoopEventsPublisher(EventPublisher, TransactionalResource):
    def publish(self, routing_key: str, payload: dict[str, Any]) -> None:
        pass

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass
