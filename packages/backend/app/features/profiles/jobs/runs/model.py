from __future__ import annotations

from datetime import datetime
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.core.database.base.immutable import ImmutableVersionedBase
from app.features.profiles.jobs.runs.domain.status import JobRunStatus

if TYPE_CHECKING:
    from app.features.profiles.jobs.model import JobORM


class RunORM(ImmutableVersionedBase):
    __tablename__ = "runs"

    job_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("jobs.id"),
        nullable=False
    )

    status: Mapped[JobRunStatus] = mapped_column(
        Enum(JobRunStatus), nullable=False, default=JobRunStatus.WAITING)

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True)

    job: Mapped["JobORM"] = relationship(
        "JobORM",
        back_populates="runs",
        lazy="selectin",
        uselist=False,
    )
