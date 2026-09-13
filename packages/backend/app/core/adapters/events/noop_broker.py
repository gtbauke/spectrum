from typing import Any
from app.core.ports.events.message_broker import MessageBroker


class NoopMessageBroker(MessageBroker):
    async def send(self, routing_key: str, payload: dict[str, Any]) -> None:
        pass
