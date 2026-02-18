from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func, DateTime
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
        DateTime(),
        nullable=False,
        default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )
