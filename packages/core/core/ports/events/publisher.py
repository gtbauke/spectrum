from typing import Protocol, Any


class EventPublisher(Protocol):
    def publish(self, routing_key: str, payload: dict[str, Any]) -> None: ...
