from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import UUID
from pydantic import BaseModel

from sqlalchemy import DateTime, Integer, String, Enum, Text, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID

from core.models.outbox.outbox import AggregateType, Outbox
from core.models.outbox.outbox_status import OutboxStatus
from core.tasks.types import TaskType

from db.base import Base


class OutboxORM(Base):
    __tablename__ = "outbox_events"

    # Aggregate metadata
    aggregate_type: Mapped[str] = mapped_column(
        String(length=100),
        nullable=False,
    )

    aggregate_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
    )

    # Event metadata
    event_type: Mapped[str] = mapped_column(
        String(length=200),
        nullable=False,
    )

    event_version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    # Event payload
    payload: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
    )

    # Outbox metadata
    status: Mapped[OutboxStatus] = mapped_column(
        Enum(OutboxStatus),
        nullable=False,
        default=OutboxStatus.PENDING,
    )

    attempts: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    last_error: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Timestamps
    available_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now,
    )

    published_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    __table_args__ = (
        Index(
            "idx_outbox_pending_available",
            "status",
            "available_at",
            "created_at",
        ),

        Index(
            "idx_outbox_aggregate",
            "aggregate_type",
            "aggregate_id",
        ),

        Index(
            "idx_outbox_event",
            "event_type",
            "event_version",
        )
    )

    @classmethod
    def from_domain[T: BaseModel](cls, outbox: Outbox[T]) -> OutboxORM:
        return cls(
            id=outbox.id,
            aggregate_type=outbox.aggregate_type,
            aggregate_id=outbox.aggregate_id,
            event_type=outbox.event_type,
            event_version=outbox.event_version,
            payload=outbox.payload.model_dump(mode="json"),
            status=outbox.status,
            attempts=outbox.attempts,
            last_error=outbox.last_error,
            available_at=outbox.available_at,
            published_at=outbox.published_at,
            created_at=outbox.created_at,
            updated_at=outbox.updated_at,
        )

    def to_domain[T: BaseModel](self, model_type: type[T]) -> Outbox[T]:
        validated_aggregate_type = AggregateType(self.aggregate_type)
        validated_event_type = TaskType(self.event_type)

        return Outbox[T](
            id=self.id,
            aggregate_type=validated_aggregate_type,
            aggregate_id=self.aggregate_id,
            event_type=validated_event_type,
            event_version=self.event_version,
            payload=model_type.model_validate(self.payload),
            status=self.status,
            attempts=self.attempts,
            last_error=self.last_error,
            available_at=self.available_at,
            published_at=self.published_at,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
