from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.features.datasets.repository import IDatasetsRepository
from core.features.datasets.dataset import Dataset
from core.features.datasets.where import DatasetWhere, DatasetFilter
from core.utils.pagination.base import Pagination
from core.utils.pagination.response import PaginatedResponse

from db.common.repositories.sql_alchemy_base_repository import SqlAlchemyBaseRepository

from .mapper import DatasetsMapper
from .model import DatasetORM


class SqlAlchemyDatasetsRepository(
    SqlAlchemyBaseRepository[DatasetORM, Dataset,
                             DatasetWhere, DatasetFilter, DatasetsMapper],
    IDatasetsRepository,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, DatasetORM, DatasetsMapper)

    async def add(self, entity: Dataset) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._add(orm)

    async def update(self, entity: Dataset) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._update(orm)

    async def delete(self, entity: Dataset) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._delete(orm)

    async def get_unique(self, where: DatasetWhere) -> Dataset | None:
        return await super()._get_unique(where)

    async def list(self, filter: DatasetFilter | None = None, pagination: Pagination | None = None) -> PaginatedResponse[Dataset]:
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
