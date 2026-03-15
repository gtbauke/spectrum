from __future__ import annotations
from uuid import UUID

from core.models.base import BaseMutableDomainModel
from core.models.jobs.job_version import JobVersion


class Job(BaseMutableDomainModel):
    owner_id: UUID
    profile_version_id: UUID

    versions: list[JobVersion]

    @classmethod
    def new(cls, owner_id: UUID, profile_version_id: UUID) -> Job:
        return cls(
            owner_id=owner_id,
            profile_version_id=profile_version_id,
            versions=[],
        )
