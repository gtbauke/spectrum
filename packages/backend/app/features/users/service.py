from typing import Optional

from app.features.users.dtos.create_user import CreateUserDTO
from app.features.users.dtos.update_user import UpdateUserDTO
from app.services.encryption import EncryptionService
from app.features.owners.service import CreateOwnerDTO, OwnersService

from .where import UsersWhere
from .errors.email_already_in_use import EmailAlreadyInUse

from core.models.users.user import User
from core.services.base import BaseCRUDService, UnitOfWork


class UsersService(BaseCRUDService[
    User,
    UsersWhere,
    CreateUserDTO,
    UpdateUserDTO,
]):
    def __init__(
        self,
        *,
        encryption_service: EncryptionService,
        owners_service: OwnersService,
    ):
        self._encryption_service = encryption_service
        self._owners_service = owners_service

    async def get_unique(
        self,
        *,
        uow: UnitOfWork,
        where: UsersWhere,
    ) -> Optional[User]:
        return await uow.users.get_unique(where=where)

    async def create(
        self,
        *,
        uow: UnitOfWork,
        data: CreateUserDTO,
    ) -> User:
        existing_user = await uow.users.get_unique(
            where=UsersWhere(email=data.email)
        )

        if existing_user:
            raise EmailAlreadyInUse(email=data.email)

        hashed = self._encryption_service.hash_password(data.password)

        user = await uow.users.add(
            User.new(
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                password_hash=hashed,
            )
        )

        await self._owners_service.create(
            uow=uow,
            data=CreateOwnerDTO.user(user_id=user.id)
        )

        return user

    async def update_unique(
        self,
        *,
        uow: UnitOfWork,
        where: UsersWhere,
        data: UpdateUserDTO,
    ) -> User:
        user = await uow.users.get_unique(where=where)

        if not user:
            raise ValueError("User not found")

        update_data = data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password_hash"] = self._encryption_service.hash_password(
                update_data.pop("password")
            )

        updated_user = user.model_copy(
            update=update_data
        )

        return await uow.users.update(updated_user)

    async def delete_unique(
        self,
        *,
        uow: UnitOfWork,
        where: UsersWhere,
    ):
        await uow.users.delete(where=where)

    async def get_all(
        self,
        *,
        uow: UnitOfWork,
    ) -> list[User]:
        return await uow.users.list_all()


def get_users_service() -> UsersService:
    encryption_service = EncryptionService()
    owners_service = OwnersService()

    return UsersService(
        encryption_service=encryption_service,
        owners_service=owners_service,
    )
