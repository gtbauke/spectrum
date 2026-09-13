from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, DateTime, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from .root import RootBase


class MutableBase(RootBase):
    """
    Base class for all ORM models in the application.
    This class provides common functionality that can be shared across all ORM models, such as automatic timestamping of created and updated records.

    Provided properties:
    - id: A unique identifier for each record, generated using PostgreSQL's `gen_random_uuid()` function.
    - created_at: A timestamp indicating when the record was created, automatically set to the current time when the record is inserted into the database.
    - updated_at: A timestamp indicating when the record was last updated, automatically set to the current time whenever the record is updated.
    """
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )
