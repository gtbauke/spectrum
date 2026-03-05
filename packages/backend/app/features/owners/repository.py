from uuid import UUID
from typing import Optional
from sqlalchemy import select, delete

from .models import OwnerORM

from core.utils.where import BaseWhere
from core.repositories.owners import BaseOwnersRepository
from core.models.owners.owner import Owner


class OwnersRepository(BaseOwnersRepository):
    async def get_unique(self, where: BaseWhere) -> Optional[Owner]:
        statement = select(OwnerORM).where(where.resolve(OwnerORM))
        result = await self._session.execute(statement)

        owner_orm = result.scalar_one_or_none()
        return owner_orm.to_domain() if owner_orm else None

    async def get_for_update(self, id: UUID) -> Optional[Owner]:
        return await self._session.get(Owner, id, with_for_update=True)

    async def add(self, obj: Owner) -> Owner:
        self._session.add(OwnerORM.from_domain(obj))

        await self._session.commit()
        return obj

    async def update(self, obj: Owner) -> Owner:
        await self._session.merge(OwnerORM.from_domain(obj))
        await self._session.commit()

        return obj

    async def delete(self, id: UUID) -> None:
        statement = delete(OwnerORM).where(OwnerORM.id == id)
        await self._session.execute(statement)

    async def list_all(self, where_id: Optional[UUID] = None) -> list[Owner]:
        if where_id:
            raise ValueError(
                "Filtering by ID is not supported for list_all method.")

        statement = select(OwnerORM)
        result = await self._session.execute(statement)

        return [owner_orm.to_domain() for owner_orm in result.scalars().all()]
