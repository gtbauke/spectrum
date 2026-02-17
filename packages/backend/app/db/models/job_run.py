from __future__ import annotations
from uuid import UUID
from typing import TYPE_CHECKING, Optional
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.domain.jobs.job_run import JobRun

if TYPE_CHECKING:
    from app.db.models.model import ModelORM


class JobRunORM(Base):
    __tablename__ = "job_runs"

    model_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("models.id", ondelete="SET NULL"),
        nullable=True,
    )

    model: Mapped["ModelORM"] = relationship(
        lazy="selectin",
    )

    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    finished_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    def to_domain(self) -> "JobRun":
        return JobRun(
            id=self.id,
            model_id=self.model_id,
            created_at=self.created_at,
            started_at=self.started_at,
            updated_at=self.updated_at,
            finished_at=self.finished_at,
        )
