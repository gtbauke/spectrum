from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.features.profiles.models.repository import IModelsRepository
from core.features.profiles.models.model import Model
from core.features.profiles.models.where import ModelWhere, ModelFilter
from core.utils.pagination.base import Pagination
from core.utils.pagination.response import PaginatedResponse

from db.common.repositories.sql_alchemy_base_repository import SqlAlchemyBaseRepository

from .mapper import ModelsMapper
from .model import ModelORM


class SqlAlchemyModelsRepository(
    SqlAlchemyBaseRepository[ModelORM, Model,
                             ModelWhere, ModelFilter, ModelsMapper],
    IModelsRepository,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ModelORM, ModelsMapper)

    async def add(self, entity: Model) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._add(orm)

    async def update(self, entity: Model) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._update(orm)

    async def delete(self, entity: Model) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._delete(orm)

    async def get_unique(self, where: ModelWhere) -> Model | None:
        return await super()._get_unique(where)

    async def list(self, filter: ModelFilter | None = None, pagination: Pagination | None = None) -> PaginatedResponse[Model]:
        resolved_filters = filter.resolve(
            self._model_class) if filter else None

        query = (
            select(self._model_class)
            .distinct()
        )

        if resolved_filters:
            query = query.where(*resolved_filters)

        if pagination:
            query = query.limit(pagination.limit).offset(pagination.offset)

        domains, total_count, current_page, total_pages, size = await self._paginate_query(
            query,
            pagination,
        )

        return PaginatedResponse(
            items=domains,
            total=total_count,
            pages=total_pages,
            page=current_page,
            size=size,
        )
