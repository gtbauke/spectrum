from typing import Protocol, Any
from pydantic import BaseModel


class EventHandler[T_Event: BaseModel](Protocol):
    routing_key: str

    def parse(self, payload: dict[str, Any]) -> T_Event: ...

    async def handle(self, event: T_Event) -> None: ...
