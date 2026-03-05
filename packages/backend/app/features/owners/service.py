from typing import Optional, Sequence

from app.features.owners.dtos.create_owner import CreateOwnerDTO
from app.features.owners.where import OwnersWhere

from core.models.owners.owner import Owner
from core.models.owners.owner_type import OwnerType
from core.services.base import BaseCRService
from core.ports.unit_of_work import UnitOfWork


class OwnersService(BaseCRService[
    Owner,
    OwnersWhere,
    CreateOwnerDTO
]):
    async def get_unique(self, *, uow: UnitOfWork, where: OwnersWhere) -> Optional[Owner]:
        return await uow.owners.get_unique(where=where)

    # TODO: when we have more owner types, we should refactor this method to handle different owner types and their specific creation logic
    async def create(self, *, uow: UnitOfWork, data: CreateOwnerDTO) -> Owner:
        if data.owner_type == OwnerType.USER and data.user_id:
            return await uow.owners.add(
                Owner.new_user(
                    user_id=data.user_id,
                )
            )

        raise NotImplementedError(
            f"Owner type {data.owner_type} is not supported yet")

    async def delete_unique(self, *, uow: UnitOfWork, where: OwnersWhere):
        owner = await uow.owners.get_unique(where=where)

        if not owner:
            raise ValueError("Owner not found")

        await uow.owners.delete(owner.id)

    async def get_all(self, *, uow: UnitOfWork) -> Sequence[Owner]:
        return await uow.owners.list_all()


def get_owners_service() -> OwnersService:
    return OwnersService()
