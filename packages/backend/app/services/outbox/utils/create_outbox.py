from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

from core.models.outbox.aggregate_type import AggregateType
from core.tasks.types import TaskType


class CreateOutboxData[Payload: BaseModel](BaseModel):
    """
    Data model for creating an outbox message.
    """
    aggregate_type: AggregateType = Field(
        ..., description="The type of the aggregate associated with the message.")

    aggregate_id: UUID = Field(
        ..., description="The unique identifier of the aggregate associated with the message.")

    event_type: TaskType = Field(
        ..., description="The type of the event represented by the message.")

    event_version: int = Field(
        ..., description="The version of the event represented by the message.")

    payload: Payload = Field(
        ..., description="The payload of the message, containing the event data.")

    available_at: datetime = Field(
        ..., description="The timestamp when the message becomes available for processing.")
