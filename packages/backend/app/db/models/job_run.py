import uuid

from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import (DateTime, func, ForeignKey)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.model import ModelORM


class JobRunORM(Base):
    __tablename__ = "job_runs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    model_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("models.id", ondelete="SET NULL"),
        nullable=True,
    )

    model: Mapped["ModelORM"] = relationship(
        back_populates="job_runs",
        lazy="selectin",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now(),
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
    )

    finished_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
    )
