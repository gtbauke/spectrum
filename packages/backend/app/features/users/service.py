from typing import Optional
from argon2 import PasswordHasher
from pydantic import SecretStr

from app.features.users.dtos.create_user import CreateUserDTO
from app.features.users.dtos.update_user import UpdateUserDTO

from .where import UsersWhere

from core.models.users.user import User
from core.services.base import BaseService, UnitOfWork


class UsersService(BaseService[
    User,
    UsersWhere,
    CreateUserDTO,
    UpdateUserDTO,
]):
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
        ph = PasswordHasher()
        hashed = ph.hash(data.password)

        return await uow.users.add(
            User.new(
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                password_hash=SecretStr(hashed),
            )
        )

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
            ph = PasswordHasher()
            update_data["password_hash"] = SecretStr(
                ph.hash(update_data.pop("password")))

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
        user = await uow.users.get_unique(where=where)

        if not user:
            raise ValueError("User not found")

        await uow.users.delete(user.id)

    async def get_all(
        self,
        *,
        uow: UnitOfWork,
    ) -> list[User]:
        return await uow.users.list_all()
