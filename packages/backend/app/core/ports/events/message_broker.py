from typing import Protocol, Any


class MessageBroker(Protocol):
    async def send(self, routing_key: str,
                   payload: dict[str, Any]) -> None: ...
