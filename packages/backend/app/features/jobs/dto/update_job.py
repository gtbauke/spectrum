from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from ..versions.dto.update_job_version import UpdateJobVersion


class UpdateJobBody(BaseModel):
    new_owner_id: Optional[UUID] = None
    version: Optional[UpdateJobVersion] = None


class UpdateJob(UpdateJobBody):
    owner_id: UUID
    profile_version_id: UUID
