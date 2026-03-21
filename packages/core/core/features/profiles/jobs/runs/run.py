from uuid import UUID
from pydantic import Field
from datetime import datetime

from core.features.base import BaseImmutableVersionedDomainModel

from .status import JobRunStatus


class Run(BaseImmutableVersionedDomainModel):
    job_id: UUID = Field(..., description="The ID of the job")

    status: JobRunStatus = Field(
        JobRunStatus.WAITING, description="The status of the job run")

    started_at: datetime | None = Field(
        None, description="The time the job run started")

    finished_at: datetime | None = Field(
        None, description="The time the job run finished")
