from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from ..versions.dto.create_job_version import CreateJobVersion


class CreateJobBody(BaseModel):
    version: Optional[CreateJobVersion]


class CreateJob(CreateJobBody):
    owner_id: UUID
    profile_version_id: UUID
