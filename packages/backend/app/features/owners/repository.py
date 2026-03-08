from typing import Optional
from sqlalchemy import select, update
from datetime import datetime, timezone

from .models import OwnerORM

from core.repositories.owners import BaseOwnersRepository
from core.models.owners.owner import Owner
from core.models.owners.where import OwnersFilter, OwnersWhere


class OwnersRepository(BaseOwnersRepository):
    async def get_unique(self, where: OwnersWhere) -> Optional[Owner]:
        statement = select(OwnerORM).where(where.resolve(OwnerORM))
        result = await self._session.execute(statement)

        owner_orm = result.scalar_one_or_none()
        return owner_orm.to_domain() if owner_orm else None

    async def get_for_update(self, where: OwnersWhere) -> Optional[Owner]:
        statement = select(OwnerORM).where(
            where.resolve(OwnerORM)).with_for_update()
        result = await self._session.execute(statement)

        owner_orm = result.scalar_one_or_none()
        return owner_orm.to_domain() if owner_orm else None

    async def add(self, obj: Owner) -> Owner:
        self._session.add(OwnerORM.from_domain(obj))

        await self._session.commit()
        return obj

    async def update(self, obj: Owner) -> Owner:
        await self._session.merge(OwnerORM.from_domain(obj))
        await self._session.commit()

        return obj

    async def delete(self, where: OwnersWhere) -> None:
        statement = update(OwnerORM).where(where.resolve(OwnerORM)).values(
            deleted_at=datetime.now(timezone.utc))

        await self._session.execute(statement)
        await self._session.commit()

    async def list_all(self, where: Optional[OwnersFilter] = None) -> list[Owner]:
        statement = select(OwnerORM)

        if where:
            conditions = where.resolve(OwnerORM)
            if len(conditions) > 0:
                statement = statement.where(*conditions)

        result = await self._session.execute(statement)

        return [owner_orm.to_domain() for owner_orm in result.scalars().all()]
