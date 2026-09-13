from typing import Iterable, Type

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database.repositories.sql_alchemy_base_repository import SqlAlchemyBaseRepository

from app.core.utils.where import BaseUniqueWhere
from app.core.utils.filters.base import BaseFilter
from app.core.domain.base import BaseMutableDomainModel

from app.core.database.base.root import RootBase
from app.core.database.mappers.base import IMapper


class SqlAlchemyBulkRepository[
    T_ORM: RootBase,
    T_Domain: BaseMutableDomainModel,
    T_Where: BaseUniqueWhere,
    T_Filter: BaseFilter,
    T_Mapper: IMapper,
](SqlAlchemyBaseRepository[T_ORM, T_Domain, T_Where, T_Filter, T_Mapper]):
    """
    Extends SqlAlchemyBaseRepository with bulk operations.
    """
    def __init__(self, session: AsyncSession, model_class: Type[T_ORM], mapper: Type[T_Mapper]) -> None:
        super().__init__(session, model_class, mapper)

    async def _add_many(self, entities: Iterable[T_ORM]) -> None:
        self._session.add_all(entities)

    async def _update_many(self, entities: Iterable[T_ORM]) -> None:
        for entity in entities:
            await self._session.merge(entity)

    async def _delete_many(self, entities: Iterable[T_ORM]) -> None:
        for entity in entities:
            tracked_entity = await self._session.merge(entity)
            await self._session.delete(instance=tracked_entity)
