from typing import Optional

from sqlalchemy import select, delete

from .models import RefreshTokenORM

from core.repositories.auth import BaseAuthRepository
from core.models.auth.refresh_token import RefreshToken
from core.models.auth.where import AuthFilter, AuthWhere
from core.utils.pagination.base import Pagination


class AuthRepository(BaseAuthRepository):
    async def get_unique(self, where: AuthWhere) -> Optional[RefreshToken]:
        statement = select(RefreshTokenORM).where(
            where.resolve(RefreshTokenORM))
        result = await self._session.execute(statement)

        refresh_token_orm = result.scalar_one_or_none()
        return refresh_token_orm.to_domain() if refresh_token_orm else None

    async def get_for_update(self, where: AuthWhere) -> Optional[RefreshToken]:
        statement = select(RefreshTokenORM).where(
            where.resolve(RefreshTokenORM)).with_for_update()
        result = await self._session.execute(statement)

        refresh_token_orm = result.scalar_one_or_none()
        return refresh_token_orm.to_domain() if refresh_token_orm else None

    async def add(self, obj: RefreshToken) -> RefreshToken:
        self._session.add(RefreshTokenORM.from_domain(obj))

        await self._session.commit()
        return obj

    async def update(self, obj: RefreshToken) -> RefreshToken:
        await self._session.merge(RefreshTokenORM.from_domain(obj))
        await self._session.commit()

        return obj

    async def delete(self, where: AuthWhere) -> None:
        statement = delete(RefreshTokenORM).where(
            where.resolve(RefreshTokenORM))

        await self._session.execute(statement)
        await self._session.commit()

    async def list_all(self, where: Optional[AuthFilter] = None,
                       pagination: Optional[Pagination] = None) -> list[RefreshToken]:
        statement = select(RefreshTokenORM)

        if where:
            statement = statement.where(*where.resolve(RefreshTokenORM))

        if pagination:
            statement = pagination.apply(statement)

        result = await self._session.execute(statement)

        return [refresh_token_orm.to_domain() for refresh_token_orm in result.scalars().all()]
