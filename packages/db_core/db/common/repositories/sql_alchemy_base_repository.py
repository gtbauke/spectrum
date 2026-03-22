import math

from typing import Type, Sequence

from sqlalchemy import select, func, Select
from sqlalchemy.orm.interfaces import ORMOption
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils.pagination.base import Pagination
from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter
from core.features.base import RootDomainModel

from db.common.base.root import RootBase
from db.common.mappers.base import IMapper


class SqlAlchemyBaseRepository[
    T_ORM: RootBase,
    T_Domain: RootDomainModel,
    T_Where: BaseUniqueWhere,
    T_Filter: BaseFilter,
    T_Mapper: IMapper,
]:
    """
    Base class for all concrete SQLAlchemy repositories.
    """

    def __init__(self, session: AsyncSession, model_class: Type[T_ORM], mapper: Type[T_Mapper]) -> None:
        self._session = session
        self._model_class = model_class
        self._mapper = mapper

    async def _get_unique(self, where: T_Where, *options: ORMOption) -> T_Domain | None:
        unique_ident = where.resolve_unique_value()
        result = await self._session.get(
            entity=self._model_class,
            ident=unique_ident,
            options=options if options else None,
        )

        if not result:
            return None

        return self._mapper.to_domain(result)

    async def _add(self, entity: T_ORM) -> None:
        self._session.add(entity)

    async def _update(self, entity: T_ORM) -> None:
        await self._session.merge(entity)

    async def _delete(self, entity: T_ORM) -> None:
        tracked_entity = await self._session.merge(entity)
        await self._session.delete(instance=tracked_entity)

    async def _paginate_query(self, query: Select[tuple[T_ORM, ...]], pagination: Pagination | None = None) -> tuple[Sequence[T_Domain], int, int, int, int]:
        """Returns (orms, total_count, current_page, total_pages, size)"""
        count_query = select(func.count()).select_from(query.subquery())
        total = await self._session.execute(count_query)
        total_count = total.scalar() or 0

        if pagination:
            query = query.limit(pagination.limit).offset(pagination.offset)

        result = await self._session.execute(query)
        orms = result.scalars().unique().all()

        domains = [self._mapper.to_domain(orm) for orm in orms]

        size = pagination.limit if pagination and pagination.limit > 0 else max(
            total_count, 1)
        offset = pagination.offset if pagination else 0
        current_page = (offset // size) + 1
        total_pages = math.ceil(total_count / size) if total_count > 0 else 0

        return domains, total_count, current_page, total_pages, size

    async def _list_all_query(self, query: Select[tuple[T_ORM, ...]]) -> Sequence[T_Domain]:
        result = await self._session.execute(query)
        orms = result.scalars().unique().all()

        return [self._mapper.to_domain(orm) for orm in orms]
