from datetime import datetime, timezone
from uuid import UUID
from fastapi import APIRouter, Depends, status, Query

from app.api.unit_of_work import get_uow
from app.features.users.errors.user_not_found import UserNotFound
from app.services.encryption import EncryptionService

from db.adapters.unit_of_work import SqlAlchemyUnitOfWork

from core.ports.unit_of_work import UnitOfWork
from core.features.users.user import User
from core.features.users.where import UserWhere, UserFilter
from core.utils.pagination.base import Pagination
from core.utils.filters.field_filter import DateTimeFilter

from .dtos.create import CreateUserDto
from .dtos.update import UpdateUserDto

users_router = APIRouter()


@users_router.post(
    "",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    description="Creates a new user"
)
async def create_user(
    dto: CreateUserDto,
    uow: UnitOfWork = Depends(get_uow),
    encryption_service: EncryptionService = Depends(EncryptionService),
):
    user = User.new(
        first_name=dto.first_name,
        last_name=dto.last_name,
        email=dto.email,
        password_hash=encryption_service.hash_password(
            dto.password.get_secret_value()),
    )

    await uow.users.add(user)
    return user


@users_router.get(
    "",
    description="Get all users with pagination"
)
async def get_users(
    limit: int = Query(50, ge=1),
    offset: int = Query(0, ge=0),
    uow: UnitOfWork = Depends(get_uow),
):
    pagination = Pagination(limit=limit, offset=offset)
    default_filter = UserFilter(deleted_at=DateTimeFilter(is_null=True))

    users_page = await uow.users.list(filter=default_filter, pagination=pagination)

    return users_page


@users_router.get(
    "/{user_id}",
    response_model=User,
    description="Get a specific user"
)
async def get_user(
    user_id: UUID,
    uow: UnitOfWork = Depends(get_uow)
):
    where = UserWhere(id=user_id)
    user = await uow.users.get_unique(where)

    if not user:
        raise UserNotFound()

    return user


@users_router.put(
    "/{user_id}",
    response_model=User,
    description="Update a user"
)
async def update_user(
    user_id: UUID,
    dto: UpdateUserDto,
    uow: UnitOfWork = Depends(get_uow),
    encryption_service: EncryptionService = Depends(EncryptionService),
):
    where = UserWhere(id=user_id)
    user = await uow.users.get_unique(where)

    if not user:
        raise UserNotFound()

    present_data = dto.model_dump(exclude_unset=True)
    if "password" in present_data:
        password_secret = present_data.pop("password")
        present_data["password_hash"] = encryption_service.hash_password(
            password_secret.get_secret_value())

    updated_user = user.model_copy(update=present_data)

    await uow.users.update(entity=updated_user)
    return updated_user


@users_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Soft delete a user"
)
async def delete_user(
    user_id: UUID,
    uow: UnitOfWork = Depends(get_uow)
):
    where = UserWhere(id=user_id)
    user = await uow.users.get_unique(where)

    if not user:
        raise UserNotFound()

    user.deleted_at = datetime.now(tz=timezone.utc)
    await uow.users.update(user)

    return None
