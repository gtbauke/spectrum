import logging
from uuid import UUID

from fastapi import APIRouter, Depends

from core.utils.filters.field_filter import DateTimeFilter

from .service import UsersService, get_users_service
from .dtos.create_user import CreateUserDTO
from .dtos.update_user import UpdateUserDTO

from core.ports.unit_of_work import UnitOfWork
from core.models.users.where import UsersWhere, UsersFilter

from app.api.unit_of_work import get_uow

logger = logging.getLogger(__name__)
users_router = APIRouter(tags=["users"])


@users_router.get("/")
async def get_users(
    uow: UnitOfWork = Depends(get_uow),
    service: UsersService = Depends(get_users_service),
):
    return await service.get_all(
        uow=uow,
        filter=UsersFilter(
            deleted_at=DateTimeFilter(is_null=True)
        )
    )


@users_router.post("/")
async def create_user(
    data: CreateUserDTO,
    uow: UnitOfWork = Depends(get_uow),
    service: UsersService = Depends(get_users_service),
):
    logger.info("CREATING USER", extra={
        "data": data.model_dump()
    })

    return await service.create(uow=uow, data=data)


@users_router.get("/{user_id}")
async def get_user(
    user_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
    service: UsersService = Depends(get_users_service),
):
    where = UsersWhere(id=user_id)
    return await service.get_unique(uow=uow, where=where)


@users_router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
    service: UsersService = Depends(get_users_service),
):
    where = UsersWhere(id=user_id)
    await service.delete_unique(uow=uow, where=where)


@users_router.put("/{user_id}")
async def update_user(
    user_id: UUID,
    data: UpdateUserDTO,
    uow: UnitOfWork = Depends(get_uow),
    service: UsersService = Depends(get_users_service),
):
    where = UsersWhere(id=user_id)
    return await service.update_unique(uow=uow, where=where, data=data)
