from uuid import UUID

from fastapi import APIRouter, Depends, status, Query

from app.api.unit_of_work import get_uow

from core.models.owners.owner_type import OwnerType
from core.ports.unit_of_work import UnitOfWork
from core.models.owners.owner import Owner

from .errors.owner_not_found import OwnerNotFound
from .service import OwnersService, OwnerWhere, get_owners_service


owners_router = APIRouter(tags=["owners"])


@owners_router.get(
    path="/{entity_id}",
    response_model=Owner,
    status_code=status.HTTP_200_OK,
)
async def get_owner(
    entity_id: UUID,
    owner_type: OwnerType = Query(
        default=OwnerType.USER, description="The type of the owner"),
    uow: UnitOfWork = Depends(get_uow),
    service: OwnersService = Depends(get_owners_service),
):
    if owner_type != OwnerType.USER:
        raise NotImplementedError(
            f"Owner type {owner_type} is not supported yet")

    owner = await service.get_unique(
        uow=uow,
        where=OwnerWhere(user_id=entity_id)
    )

    if not owner:
        raise OwnerNotFound(entity_id=entity_id)

    return owner
