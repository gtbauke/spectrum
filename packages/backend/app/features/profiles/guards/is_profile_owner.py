from fastapi import Depends
from uuid import UUID

from core.ports.unit_of_work import UnitOfWork
from core.models.profiles.where import ProfilesWhere

from app.api.unit_of_work import get_uow
from app.features.auth.errors.forbidden import Forbidden
from app.features.auth.guards.get_current_user import get_current_owner

from ..errors.profile_not_found import ProfileNotFound


async def is_profile_owner(
    profile_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
    current_owner: UUID = Depends(get_current_owner),
):
    owner_id = await uow.profiles.get_owner_id(where=ProfilesWhere(id=profile_id))

    if not owner_id:
        raise ProfileNotFound()

    if owner_id != current_owner:
        raise Forbidden()

    return owner_id
