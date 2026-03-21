import math

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.owners.repository import IOwnersRepository
from core.models.owners.where import OwnerWhere, OwnerFilter
from core.models.owners.owner import Owner
from core.utils.pagination.base import Pagination
from core.utils.pagination.response import PaginatedResponse

from db.common.repositories.sql_alchemy_base_repository import SqlAlchemyBaseRepository

from .model import OwnerORM


class SqlAlchemyOwnersRepository(
    SqlAlchemyBaseRepository[OwnerORM],
    IOwnersRepository
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, OwnerORM)

    async def get_unique(self, where: OwnerWhere) -> Owner | None:
        ident = where.resolve_unique_value()
        entity = await self._session.get(self._model_class, ident)

        return entity.to_domain() if entity else None

    async def add(self, entity: Owner) -> None:
        orm = self._model_class.from_domain(entity)

        self._session.add(orm)
        await self._session.flush()

    async def list(self, filter: OwnerFilter | None = None, pagination: Pagination | None = None) -> PaginatedResponse[Owner]:
        resolved_filters = filter.resolve(
            self._model_class) if filter else None

        total_query = (
            select(func.count())
            .select_from(self._model_class)
        )

        if resolved_filters:
            total_query = total_query.where(*resolved_filters)

        total = await self._session.execute(total_query)
        total_count = total.scalar() or 0

        query = (
            select(self._model_class)
            .options(
                selectinload(self._model_class.user)
            )
            .distinct()
        )

        if resolved_filters:
            query = query.where(*resolved_filters)

        if pagination:
            query = query.limit(pagination.limit).offset(pagination.offset)

        result = await self._session.execute(query)
        orms = result.scalars()

        items = [orm.to_domain() for orm in orms]

        size = pagination.limit if pagination and pagination.limit > 0 else max(
            total_count, 1)
        offset = pagination.offset if pagination else 0

        current_page = (offset // size) + 1
        total_pages = math.ceil(total_count / size) if total_count > 0 else 0

        return PaginatedResponse(
            items=items,
            total=total_count,
            pages=total_pages,
            page=current_page,
            size=size,
        )
