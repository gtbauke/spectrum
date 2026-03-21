from __future__ import annotations

from uuid import UUID
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from core.models.job_runs.job_run_status import JobRunStatus
from core.models.job_runs.job_run import JobRun

from db.common.base.immutable import ImmutableBase

if TYPE_CHECKING:
    from app.features.jobs.models import JobORM


class JobRunORM(ImmutableBase):
    __tablename__ = "job_runs"

    job_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("jobs.id"),
        nullable=False,
    )

    job: Mapped["JobORM"] = relationship(
        "JobORM",
        back_populates="runs"
    )

    job_run_status: Mapped[JobRunStatus] = mapped_column(
        Enum(JobRunStatus),
        nullable=False,
    )

    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    finished_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    @classmethod
    def from_domain(cls, domain_obj: JobRun) -> JobRunORM:
        return cls(
            id=domain_obj.id,
            timestamp=domain_obj.timestamp,
            job_id=domain_obj.job_id,
            job_run_status=domain_obj.job_run_status,
            started_at=domain_obj.started_at,
            finished_at=domain_obj.finished_at,
        )

    def to_domain(self) -> JobRun:
        return JobRun(
            id=self.id,
            timestamp=self.timestamp,
            job_id=self.job_id,
            job_run_status=self.job_run_status,
            started_at=self.started_at,
            finished_at=self.finished_at,
        )
