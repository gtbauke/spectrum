from typing import Optional
from uuid import UUID

from sqlalchemy import select, delete

from .models import RefreshTokenORM

from core.repositories.auth import BaseAuthRepository
from core.utils.where import BaseWhere
from core.models.auth.refresh_token import RefreshToken


class AuthRepository(BaseAuthRepository):
    async def get_unique(self, where: BaseWhere) -> Optional[RefreshToken]:
        statement = select(RefreshTokenORM).where(
            where.resolve(RefreshTokenORM))
        result = await self._session.execute(statement)

        refresh_token_orm = result.scalar_one_or_none()
        return refresh_token_orm.to_domain() if refresh_token_orm else None

    async def get_for_update(self, id: UUID) -> Optional[RefreshToken]:
        refresh_token_orm = await self._session.get(RefreshTokenORM, id, with_for_update=True)
        return refresh_token_orm.to_domain() if refresh_token_orm else None

    async def add(self, obj: RefreshToken) -> RefreshToken:
        self._session.add(RefreshTokenORM.from_domain(obj))

        await self._session.commit()
        return obj

    async def update(self, obj: RefreshToken) -> RefreshToken:
        await self._session.merge(RefreshTokenORM.from_domain(obj))
        await self._session.commit()

        return obj

    async def delete(self, id: UUID) -> None:
        statement = delete(RefreshTokenORM).where(RefreshTokenORM.id == id)
        await self._session.execute(statement)
        await self._session.commit()

    async def list_all(self, where_id: Optional[UUID] = None) -> list[RefreshToken]:
        if where_id:
            raise ValueError(
                "Filtering by ID is not supported for list_all method.")

        statement = select(RefreshTokenORM)
        result = await self._session.execute(statement)

        return [refresh_token_orm.to_domain() for refresh_token_orm in result.scalars().all()]
