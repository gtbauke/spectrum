from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import func, DateTime, UniqueConstraint, Index, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class Base(DeclarativeBase):
    """
    Base class for all ORM models in the application.
    This class provides common functionality that can be shared across all ORM models, such as automatic timestamping of created and updated records.
    """
    __abstract__ = True

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
    __abstract__ = True

    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class ImmutableBase(DeclarativeBase):
    """
    This class is a base class for all immutable models that require timestamping of creation time.
    It provides a `timestamp` field that is automatically set to the current time when a new record is created.

    Provided properties:
    - `id`: A unique identifier for the record, generated using UUID4.
    - `version`: An integer field that can be used for optimistic concurrency control, defaulting to 1.
    - `is_latest`: A boolean field that indicates whether this record is the latest version, defaulting to True.
    - `timestamp`: A datetime field that records the time when the record was created, automatically set to the current time.

    Constraints and indexes:
    - Unique constraint on the combination of `id` and `version` to ensure that each version of a record is unique.
    - Index on `id` and `version` for efficient querying of specific versions of a record.
    - Index on `is_latest` for efficient querying of the latest versions of records.
    """
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    version: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
    )

    is_latest: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
    )

    @declared_attr.directive
    def __table_args__(cls):
        return (
            UniqueConstraint(
                "id", "version", name=f"uq_{cls.__tablename__}_id_version"),
            Index(f"idx_{cls.__tablename__}_id_version", "id", "version"),
            Index(f"idx_{cls.__tablename__}_is_latest", "is_latest"),
        )
