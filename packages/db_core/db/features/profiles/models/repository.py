from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

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
        await super()._add(entity=orm)

    async def update(self, entity: Model) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._update(entity=orm)

    async def delete(self, entity: Model) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._delete(entity=orm)

    async def get_unique(self, where: ModelWhere) -> Model | None:
        return await super()._get_unique(where=where)

    def _build_query(
        self,
        filter: ModelFilter | None = None,
    ):
        resolved_filters = filter.resolve(
            self._model_class) if filter else None

        query = select(self._model_class).distinct()

        if resolved_filters:
            query = query.where(*resolved_filters)
            
        return query

    async def list(
        self,
        filter: ModelFilter | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[Model]:
        query = self._build_query(filter=filter)

        if pagination:
            query = query.limit(limit=pagination.limit).offset(offset=pagination.offset)

        domains, total_count, current_page, total_pages, size = await self._paginate_query(
            query=query,
            pagination=pagination,
        )

        return PaginatedResponse(
            items=domains,
            total=total_count,
            pages=total_pages,
            page=current_page,
            size=size,
        )

    async def list_all(
        self,
        filter: ModelFilter | None = None,
    ) -> Sequence[Model]:
        query = self._build_query(filter=filter)
        return await self._list_all_query(query=query)
