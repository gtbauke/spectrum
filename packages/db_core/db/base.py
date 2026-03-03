from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func, DateTime, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class Base(DeclarativeBase):
    """
    Base class for all ORM models in the application.
    This class provides common functionality that can be shared across all ORM models, such as automatic timestamping of created and updated records.
    """

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )


class SoftDeleteMixin:
    """
    Mixin class for soft deletion of records.
    This class provides a `deleted_at` field that can be used to mark records as deleted without actually removing them from the database.
    """

    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class ImmutableBase(DeclarativeBase):
    """
    This class is a base class for all immutable models that require timestamping of creation time.
    It provides a `timestamp` field that is automatically set to the current time when a new record is created.
    """

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    version: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
    )

    __table_args__ = (
        UniqueConstraint("id", "version", name="uq_id_version"),
        Index("idx_id_version", "id", "version"),
        Index("idx_timestamp", "timestamp"),
    )
