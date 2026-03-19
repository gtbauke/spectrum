from datetime import datetime, timezone
from typing import Optional
from uuid import UUID
from pydantic import Field

from core.models.base import BaseImmutableDomainModel
from core.models.job_runs.job_run_status import JobRunStatus


class JobRun(BaseImmutableDomainModel):
    job_id: UUID = Field(..., description="The job id for this job run")

    job_run_status: JobRunStatus = Field(...,
                                         description="The type of job run")

    started_at: Optional[datetime] = Field(
        ..., description="Date and time the job started running")

    finished_at: Optional[datetime] = Field(
        ..., description="Date and time the job finished running")

    @classmethod
    def new(cls, *, job_id: UUID):
        return cls(
            job_id=job_id,
            job_run_status=JobRunStatus.WAITING,
            started_at=None,
            finished_at=None,
        )
