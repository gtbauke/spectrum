from typing import Optional
from uuid import UUID

from fastapi import Depends

from app.features.auth.errors.forbidden import Forbidden
from app.features.profiles.router import get_optional_current_owner
from app.features.profiles.versions.errors.profile_version_not_found import ProfileVersionNotFound
from app.api.unit_of_work import get_uow

from core.models.profiles.where import ProfileVersionWhere, ProfileWhere
from core.ports.unit_of_work import UnitOfWork


async def can_edit_profile(
    profile_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
    current_owner: Optional[UUID] = Depends(get_optional_current_owner),
):
    latest_profile_version = await uow.profile_versions.get_unique(
        where=ProfileVersionWhere(
            profile_id=profile_id,
            is_latest=True,
        )
    )

    if not latest_profile_version:
        raise ProfileVersionNotFound()

    if not current_owner:
        raise Forbidden()

    current_profile_owner = await uow.profiles.get_owner_id(
        where=ProfileWhere(
            id=profile_id
        )
    )

    if current_profile_owner != current_owner:
        raise Forbidden()

    return True
