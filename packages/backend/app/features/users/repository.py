from uuid import UUID
from typing import Optional
from sqlalchemy import select, delete


from .models import UserORM

from core.utils.where import BaseWhere
from core.repositories.users import BaseUsersRepository
from core.models.users.user import User


class UsersRepository(BaseUsersRepository):
    async def get_unique(self, where: BaseWhere) -> Optional[User]:
        statement = select(UserORM).where(where.resolve(UserORM))
        result = await self._session.execute(statement)

        user_orm = result.scalar_one_or_none()
        return user_orm.to_domain() if user_orm else None

    async def get_for_update(self, id: UUID) -> Optional[User]:
        return await self._session.get(User, id, with_for_update=True)

    async def add(self, obj: User) -> User:
        self._session.add(UserORM.from_domain(obj))

        await self._session.commit()
        return obj

    async def update(self, obj: User) -> User:
        await self._session.merge(UserORM.from_domain(obj))
        await self._session.commit()

        return obj

    async def delete(self, id: UUID) -> None:
        statement = delete(UserORM).where(UserORM.id == id)
        await self._session.execute(statement)

    async def list_all(self, where_id: Optional[UUID] = None) -> list[User]:
        if where_id:
            raise ValueError(
                "Filtering by ID is not supported for list_all method.")

        statement = select(UserORM)
        result = await self._session.execute(statement)

        return [user_orm.to_domain() for user_orm in result.scalars().all()]
