from __future__ import annotations

import uuid

from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Enum, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.domain.jobs.job_status import JobStatus
from app.domain.jobs.job import Job

if TYPE_CHECKING:
    from app.db.models.dataset import DatasetORM
    from app.db.models.model import ModelORM


class JobORM(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    status: Mapped[JobStatus] = mapped_column(
        Enum(
            JobStatus,
            name="job_status",
        ),
        nullable=False,
        default=JobStatus.PENDING,
    )

    dataset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("datasets.id", ondelete="CASCADE"),
        nullable=False,
    )

    dataset: Mapped["DatasetORM"] = relationship(
        back_populates="jobs",
        lazy="selectin",
    )

    models: Mapped[list["ModelORM"]] = relationship(
        back_populates="job",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now(),
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    def to_domain(self) -> Job:
        return Job(
            id=self.id,
            status=self.status,
            dataset_id=self.dataset_id,
            dataset=self.dataset.to_domain(),
            created_at=self.created_at,
            started_at=self.started_at,
            finished_at=self.finished_at,
            models=[model.to_domain() for model in self.models],
        )

    @classmethod
    def from_domain(cls, job: Job) -> JobORM:
        return cls(
            id=job.id,
            status=job.status,
            dataset_id=job.dataset_id,
            created_at=job.created_at,
            started_at=job.started_at,
            finished_at=job.finished_at,
            models=[ModelORM.from_domain(model) for model in job.models],
        )
