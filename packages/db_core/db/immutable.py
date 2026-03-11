from typing import Any
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, declared_attr
from sqlalchemy import func, DateTime, UniqueConstraint, Index, Boolean, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from .root import RootBase


class ImmutableBase(RootBase):
    """
    Base class for all immutable ORM models in the application.
    This class provides common functionality that can be shared across all immutable ORM models, such as automatic
    timestamping of created records.

    Defined properties:
    - `id`: A unique identifier for each record, generated using PostgreSQL's `gen_random_uuid()` function.
    - `timestamp`: A timestamp indicating when the record was created, automatically set to the current time when the record is inserted into the database.

    The class also defines a unique constraint on the `id` field and an index on the `timestamp` field to optimize query performance.
    """
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    @declared_attr.directive
    def __table_args__(cls) -> Any:
        return (
            UniqueConstraint("id", name=f"uq_{cls.__tablename__}_id"),
            Index(f"idx_{cls.__tablename__}_timestamp", "timestamp"),
        )


class ImmutableVersionedBase(RootBase):
    """
    Base class for all immutable ORM models in the application.
    This class provides common functionality that can be shared across all immutable ORM models, such as automatic
    timestamping of created records and versioning for optimistic concurrency control.

    Defined properties:
    - `id`: A unique identifier for each record, generated using PostgreSQL's `gen_random_uuid()` function.
    - `version`: An integer field used for optimistic concurrency control, allowing multiple versions of a record to exist while ensuring that updates are applied to the correct version.
    - `is_latest`: A boolean field indicating whether the record is the latest version.
    - `timestamp`: A timestamp indicating when the record was created, automatically set to the current time when the record is inserted into the database.

    The class also defines a unique constraint on the combination of `id` and `version`, as well as indexes on the `id`, `version`, and `is_latest` fields to optimize query performance.
    """
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    version: Mapped[int] = mapped_column(
        nullable=False,
        # primary_key=True,
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
        server_default=func.now(),
    )

    @declared_attr.directive
    def __table_args__(cls) -> Any:
        return (
            UniqueConstraint(
                "id", "version", name=f"uq_{cls.__tablename__}_id_version"),
            Index(f"idx_{cls.__tablename__}_id_version", "id", "version"),
            Index(f"idx_{cls.__tablename__}_is_latest", "is_latest"),
            Index(f"idx_{cls.__tablename__}_latest", "id",
                  unique=True, postgresql_where=text("is_latest = true"))
        )
