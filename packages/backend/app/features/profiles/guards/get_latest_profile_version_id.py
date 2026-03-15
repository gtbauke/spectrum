from uuid import UUID
from fastapi import Depends

from core.models.profiles.where import ProfileVersionWhere
from core.ports.unit_of_work import UnitOfWork

from app.api.unit_of_work import get_uow
from app.features.profiles.errors.profile_not_found import ProfileNotFound


async def get_latest_profile_version_id(
    profile_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
):
    latest_version = await uow.profile_versions.get_unique(
        where=ProfileVersionWhere(
            profile_id=profile_id,
            is_latest=True,
        )
    )

    if not latest_version:
        raise ProfileNotFound()

    return latest_version.id
