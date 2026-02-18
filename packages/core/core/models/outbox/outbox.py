from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from core.models.base import BaseDomainModel
from core.models.outbox.outbox_status import OutboxStatus
from core.models.outbox.aggregate_type import AggregateType
from core.tasks.types import TaskType


class Outbox[Payload: BaseModel](BaseDomainModel):
    """
    The Outbox model represents a message that is to be sent to an external system.
    It is used to implement the Outbox pattern, which ensures reliable message delivery
    even in the face of failures.
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

    def publish(self):
        """Marks the message as published and sets the published_at timestamp."""
        self.status = OutboxStatus.PROCESSED

        self.published_at = datetime.now()
        self.updated_at = datetime.now()

    def fail(self, error_message: str):
        """Marks the message as failed, increments the attempts counter, and sets the last_error message."""

        self.status = OutboxStatus.FAILED
        self.attempts += 1
        self.last_error = error_message

        self.updated_at = datetime.now()

    @classmethod
    def create(
        cls,
        *,
        aggregate_type: AggregateType,
        aggregate_id: UUID,
        event_type: TaskType,
        event_version: int,
        payload: Payload,
        available_at: datetime,
    ) -> Outbox[Payload]:
        return cls(
            id=uuid4(),
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            event_type=event_type,
            event_version=event_version,
            payload=payload,
            status=OutboxStatus.PENDING,
            attempts=0,
            last_error=None,
            available_at=available_at,
            published_at=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
