from pydantic import BaseModel
from typing import TypeVar, Generic


T = TypeVar("T")


class EventEnvelope(BaseModel, Generic[T]):
    event: str
    payload: T
