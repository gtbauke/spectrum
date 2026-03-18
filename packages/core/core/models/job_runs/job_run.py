from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import Field

from core.models.base import BaseImmutableDomainModel
from core.models.job_runs.job_run_type import JobRunType


class JobRun(BaseImmutableDomainModel):
    job_id: UUID = Field(..., description="The job id for this job run")

    job_run_type: JobRunType = Field(..., description="The type of job run")

    started_at: Optional[datetime] = Field(
        ..., description="Date and time the job started running")

    finished_at: Optional[datetime] = Field(
        ..., description="Date and time the job finished running")
