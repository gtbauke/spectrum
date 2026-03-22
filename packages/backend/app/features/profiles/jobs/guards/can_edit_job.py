from fastapi import Depends
from uuid import UUID

from core.ports.unit_of_work import UnitOfWork

from app.api.unit_of_work import get_uow
from app.features.profiles.jobs.errors.job_not_found import JobNotFound
from app.features.profiles.guards.can_edit_profile import can_edit_profile

from core.features.profiles.jobs.where import JobWhere


async def can_edit_job(
    profile_id: UUID,
    job_id: UUID,
    uow: UnitOfWork = Depends(dependency=get_uow),
    _: None = Depends(dependency=can_edit_profile),
) -> None:
    job = await uow.jobs.get_unique(where=JobWhere(id=job_id))

    if not job or job.profile_id != profile_id:
        raise JobNotFound()
