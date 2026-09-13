from datetime import datetime, timezone
from uuid import UUID

from app.core.ports.unit_of_work import UnitOfWork
from app.core.utils.filters.field_filter import DateTimeFilter
from app.core.utils.pagination.base import Pagination
from app.core.utils.pagination.response import PaginatedResponse
from app.features.users.domain.user import User
from app.features.users.domain.where import UserWhere, UserFilter
from app.features.users.dtos.create import CreateUserDto
from app.features.users.dtos.update import UpdateUserDto
from app.features.users.errors.user_not_found import UserNotFound
from app.services.encryption import EncryptionService


class UsersService:
    def __init__(
        self,
        uow: UnitOfWork,
        encryption_service: EncryptionService | None = None,
    ) -> None:
        self._uow = uow
        self._encryption_service = encryption_service or EncryptionService()

    async def create_user(self, dto: CreateUserDto) -> User:
        user = User.new(
            first_name=dto.first_name,
            last_name=dto.last_name,
            email=dto.email,
            password_hash=self._encryption_service.hash_password(
                dto.password.get_secret_value()
            ),
        )
        await self._uow.users.add(user)
        return user

    async def get_users(
        self,
        pagination: Pagination,
        filter: UserFilter | None = None,
    ) -> PaginatedResponse[User]:
        active_filter = filter or UserFilter(deleted_at=DateTimeFilter(is_null=True))
        return await self._uow.users.list(filter=active_filter, pagination=pagination)

    async def get_user_by_id(self, user_id: UUID) -> User:
        user = await self._uow.users.get_unique(UserWhere(id=user_id))
        if not user or user.deleted_at is not None:
            raise UserNotFound()
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        return await self._uow.users.get_unique(UserWhere(email=email))

    async def update_user(self, user_id: UUID, dto: UpdateUserDto) -> User:
        user = await self.get_user_by_id(user_id)

        present_data = dto.model_dump(exclude_unset=True)
        if "password" in present_data:
            password_secret = present_data.pop("password")
            present_data["password_hash"] = self._encryption_service.hash_password(
                password_secret.get_secret_value()
            )

        updated_user = user.model_copy(update=present_data)
        await self._uow.users.update(entity=updated_user)
        return updated_user

    async def delete_user(self, user_id: UUID) -> None:
        user = await self.get_user_by_id(user_id)
        user.deleted_at = datetime.now(tz=timezone.utc)
        await self._uow.users.update(user)
