import logging

from typing import Any, Literal, Optional, Type, Union
from abc import ABC
from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload, QueryableAttribute

from db.root import RootBase

from core.repositories.base import BaseRepository
from core.models.base import RootDomainModel
from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter
from core.utils.pagination.base import Pagination

logger = logging.getLogger(__name__)

_AttrType = Union[Literal["*"], QueryableAttribute[Any]]


class BaseRepositoryImplementation[
    DomainType: RootDomainModel,
    OrmType: RootBase,
    WhereType: BaseUniqueWhere,
    FilterType: BaseFilter,
](BaseRepository[DomainType, WhereType, FilterType], ABC):
    orm_model: Type[OrmType]
    join_on_fields: list[_AttrType] = []

    @property
    def session(self):
        return self._session

    async def get_unique(self, where: WhereType) -> Optional[DomainType]:
        statement = select(self.orm_model).where(where.resolve(self.orm_model))
        for model in self.join_on_fields:
            statement = statement.options(selectinload(model))

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

    async def add(self, obj: DomainType, commit: bool = False) -> DomainType:
        self._session.add(self.orm_model.from_domain(obj))
        await self._session.flush()

        if commit:
            await self._session.commit()

        return obj

    async def update(self, obj: DomainType, commit: bool = True) -> DomainType:
        await self._session.merge(self.orm_model.from_domain(obj))

        if commit:
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
        logger.info("LIST ALL", extra={
            "where": where,
            "statement": statement,
        })

        return [obj_orm.to_domain() for obj_orm in result.scalars().all()]
