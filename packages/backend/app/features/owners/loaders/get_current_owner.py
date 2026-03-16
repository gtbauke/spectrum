from uuid import UUID
from fastapi import Depends

from core.models.owners.owner import Owner
from core.models.owners.where import OwnerWhere
from core.ports.unit_of_work import UnitOfWork

from app.api.unit_of_work import get_uow
from app.features.owners.errors.owner_not_found import OwnerNotFound
from app.features.auth.guards.get_current_user import (
    get_current_owner as get_current_owner_id,
)


async def get_current_owner(
    uow: UnitOfWork = Depends(get_uow),
    current_owner_id: UUID = Depends(get_current_owner_id),
) -> Owner:
    owner = await uow.owners.get_unique(
        where=OwnerWhere(
            id=current_owner_id,
        )
    )

    if not owner:
        raise OwnerNotFound(current_owner_id)

    return owner
