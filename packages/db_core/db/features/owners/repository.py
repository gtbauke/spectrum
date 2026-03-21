from sqlalchemy import select
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
    SqlAlchemyBaseRepository[OwnerORM, OwnerWhere, OwnerFilter],
    IOwnersRepository,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, OwnerORM)

    async def get_unique(self, where: OwnerWhere) -> Owner | None:
        entity = await super()._get_unique(where)
        return entity.to_domain() if entity else None

    async def add(self, entity: Owner) -> None:
        orm = self._model_class.from_domain(entity)
        await super()._add(orm)

    async def list(self, filter: OwnerFilter | None = None, pagination: Pagination | None = None) -> PaginatedResponse[Owner]:
        resolved_filters = filter.resolve(
            self._model_class) if filter else None

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

        orms, total_count, current_page, total_pages, size = await self._paginate_query(
            query,
            pagination,
        )

        return PaginatedResponse(
            items=[orm.to_domain() for orm in orms],
            total=total_count,
            pages=total_pages,
            page=current_page,
            size=size,
        )
