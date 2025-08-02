from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from enum import Enum
from datetime import datetime, timezone
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from app.resources.jobs.models import Job


class JobRunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobRun(SQLModel, table=True):
    __tablename__ = "job_runs"  # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    job_id: UUID = Field(foreign_key="jobs.id")
    job: "Job" = Relationship(back_populates="runs")

    status: JobRunStatus = Field(index=True)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))

    finished_at: datetime | None = Field(default=None, nullable=True)
