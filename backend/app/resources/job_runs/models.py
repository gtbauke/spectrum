from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from enum import Enum
from datetime import datetime
from uuid import UUID, uuid4

from app.utils.sql_model_base import ModelBase

if TYPE_CHECKING:
    from app.resources.jobs.models import Job


class JobRunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobRunBase(ModelBase):
    job_id: UUID = Field(foreign_key="jobs.id")
    status: JobRunStatus = Field(index=True, default=JobRunStatus.PENDING)
    finished_at: datetime | None = Field(default=None, nullable=True)


class CreateJobRun(JobRunBase):
    pass


class UpdateJobRun(SQLModel):
    status: JobRunStatus | None = Field(default=None, nullable=True)
    finished_at: datetime | None = Field(default=None, nullable=True)


class JobRun(JobRunBase, table=True):
    __tablename__ = "job_runs"  # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    job: "Job" = Relationship(back_populates="runs")
