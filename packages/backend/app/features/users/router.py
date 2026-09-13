from uuid import UUID
from fastapi import APIRouter, Depends, status, Query

from app.api.unit_of_work import get_uow
from app.core.ports.unit_of_work import UnitOfWork
from app.core.utils.pagination.base import Pagination
from app.core.utils.pagination.response import PaginatedResponse
from app.features.users.domain.user import User
from app.features.users.dtos.create import CreateUserDto
from app.features.users.dtos.update import UpdateUserDto
from app.features.users.service import UsersService
from app.services.encryption import EncryptionService

users_router = APIRouter()


def get_users_service(
    uow: UnitOfWork = Depends(get_uow),
    encryption_service: EncryptionService = Depends(EncryptionService),
) -> UsersService:
    return UsersService(uow=uow, encryption_service=encryption_service)


@users_router.post(
    "",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    description="Creates a new user"
)
async def create_user(
    dto: CreateUserDto,
    service: UsersService = Depends(get_users_service),
):
    return await service.create_user(dto)


@users_router.get(
    "",
    response_model=PaginatedResponse[User],
    description="Get all users with pagination"
)
async def get_users(
    limit: int = Query(50, ge=1),
    offset: int = Query(0, ge=0),
    service: UsersService = Depends(get_users_service),
):
    pagination = Pagination(limit=limit, offset=offset)
    return await service.get_users(pagination=pagination)


@users_router.get(
    "/{user_id}",
    response_model=User,
    description="Get a specific user"
)
async def get_user(
    user_id: UUID,
    service: UsersService = Depends(get_users_service),
):
    return await service.get_user_by_id(user_id)


@users_router.put(
    "/{user_id}",
    response_model=User,
    description="Update a user"
)
async def update_user(
    user_id: UUID,
    dto: UpdateUserDto,
    service: UsersService = Depends(get_users_service),
):
    return await service.update_user(user_id, dto)


@users_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Soft delete a user"
)
async def delete_user(
    user_id: UUID,
    service: UsersService = Depends(get_users_service),
):
    await service.delete_user(user_id)
    return None
