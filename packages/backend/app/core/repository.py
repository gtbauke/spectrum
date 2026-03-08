from typing import Optional, Type
from abc import ABC
from datetime import datetime, timezone

from sqlalchemy import select, update

from db.root import RootBase

from core.repositories.base import BaseRepository
from core.models.base import RootDomainModel
from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter
from core.utils.pagination.base import Pagination


class BaseRepositoryImplementation[
    DomainType: RootDomainModel,
    OrmType: RootBase,
    WhereType: BaseUniqueWhere,
    FilterType: BaseFilter,
](BaseRepository[DomainType, WhereType, FilterType], ABC):
    orm_model: Type[OrmType]

    async def get_unique(self, where: WhereType) -> Optional[DomainType]:
        statement = select(self.orm_model).where(where.resolve(self.orm_model))
        result = await self._session.execute(statement)

        obj_orm = result.scalar_one_or_none()
        return obj_orm.to_domain() if obj_orm else None

    async def get_for_update(
            self, where: WhereType) -> Optional[DomainType]:
        statement = select(self.orm_model).where(
            where.resolve(self.orm_model)).with_for_update()

        result = await self._session.execute(statement)
        obj_orm = result.scalar_one_or_none()

        return obj_orm.to_domain() if obj_orm else None

    async def add(self, obj: DomainType) -> DomainType:
        self._session.add(self.orm_model.from_domain(obj))

        await self._session.commit()
        return obj

    async def update(self, obj: DomainType) -> DomainType:
        await self._session.merge(self.orm_model.from_domain(obj))
        await self._session.commit()

        return obj

    async def delete(self, where: WhereType) -> None:
        statement = update(self.orm_model).where(
            where.resolve(self.orm_model)).values(deleted_at=datetime.now(timezone.utc))

        await self._session.execute(statement)
        await self._session.commit()

    async def list_all(self, where: Optional[FilterType] = None,
                       pagination: Optional[Pagination] = None) -> list[DomainType]:
        statement = select(self.orm_model)

        if where:
            conditions = where.resolve(self.orm_model)
            if len(conditions) > 0:
                statement = statement.where(*conditions)

        if pagination:
            statement = pagination.apply(statement)

        result = await self._session.execute(statement)
        return [obj_orm.to_domain() for obj_orm in result.scalars().all()]


class BaseImmutableRepositoryImplementation[
    DomainType: RootDomainModel,
    OrmType: RootBase,
    WhereType: BaseUniqueWhere,
    FilterType: BaseFilter,
](BaseRepositoryImplementation[DomainType, OrmType, WhereType, FilterType], ABC):
    async def update(self, obj: DomainType) -> DomainType:
        raise NotImplementedError(
            "Update operation is not supported for immutable entities.")
