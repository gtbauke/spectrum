from fastapi import Depends
from uuid import UUID

from core.ports.unit_of_work import UnitOfWork

from app.api.unit_of_work import get_uow
from app.features.profiles.errors.profile_not_found import ProfileNotFound
from app.features.auth.errors.forbidden import Forbidden
from app.features.auth.guards.get_current_user import get_current_user

from core.features.profiles.where import ProfileWhere


async def can_edit_profile(
    profile_id: UUID,
    current_user_id: UUID = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
) -> None:
    profile = await uow.profiles.get_unique(ProfileWhere(id=profile_id))

    if not profile:
        raise ProfileNotFound()

    if profile.owner_id != current_user_id:
        raise Forbidden()
