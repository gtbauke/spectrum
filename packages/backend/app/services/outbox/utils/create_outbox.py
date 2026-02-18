from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

from core.models.outbox.aggregate_type import AggregateType
from core.models.outbox.outbox_status import OutboxStatus
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

    status: OutboxStatus = Field(...,
                                 description="The status of the message in the outbox.")

    attempts: int = Field(...,
                          description="The number of attempts made to send the message.")

    last_error: Optional[str] = Field(
        None, description="The last error message encountered when trying to send the message, if any.")

    available_at: datetime = Field(
        ..., description="The timestamp when the message becomes available for processing.")

    published_at: Optional[datetime] = Field(
        None, description="The timestamp when the message was successfully published, if applicable.")
