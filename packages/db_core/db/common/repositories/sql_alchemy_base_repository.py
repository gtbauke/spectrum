import math

from typing import Type, Sequence

from sqlalchemy import select, func, Select
from sqlalchemy.orm.interfaces import ORMOption
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils.pagination.base import Pagination
from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter

from db.common.base.root import RootBase


class SqlAlchemyBaseRepository[
    T_ORM: RootBase,
    T_Where: BaseUniqueWhere,
    T_Filter: BaseFilter,
]:
    """
    Base class for all concrete SQLAlchemy repositories.
    """

    def __init__(self, session: AsyncSession, model_class: Type[T_ORM]) -> None:
        self._session = session
        self._model_class = model_class

    async def _get_unique(self, where: T_Where, *options: ORMOption) -> T_ORM | None:
        unique_ident = where.resolve_unique_value()
        return await self._session.get(
            entity=self._model_class,
            ident=unique_ident,
            options=options if options else None,
        )

    async def _add(self, entity: T_ORM) -> None:
        self._session.add(entity)

    async def _update(self, entity: T_ORM) -> None:
        await self._session.merge(entity)

    async def _delete(self, entity: T_ORM) -> None:
        await self._session.delete(entity)

    async def _paginate_query(self, query: Select[tuple[T_ORM, ...]], pagination: Pagination | None = None) -> tuple[Sequence[T_ORM], int, int, int, int]:
        """Returns (orms, total_count, current_page, total_pages, size)"""
        count_query = select(func.count()).select_from(query.subquery())
        total = await self._session.execute(count_query)
        total_count = total.scalar() or 0

        if pagination:
            query = query.limit(pagination.limit).offset(pagination.offset)

        result = await self._session.execute(query)
        orms = result.scalars().unique().all()

        size = pagination.limit if pagination and pagination.limit > 0 else max(
            total_count, 1)
        offset = pagination.offset if pagination else 0
        current_page = (offset // size) + 1
        total_pages = math.ceil(total_count / size) if total_count > 0 else 0

        return orms, total_count, current_page, total_pages, size
