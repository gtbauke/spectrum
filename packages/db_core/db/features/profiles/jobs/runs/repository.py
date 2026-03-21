from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.features.profiles.jobs.runs.repository import IRunsRepository
from core.features.profiles.jobs.runs.run import Run
from core.features.profiles.jobs.runs.where import RunWhere, RunFilter
from core.utils.pagination.base import Pagination
from core.utils.pagination.response import PaginatedResponse

from db.common.repositories.sql_alchemy_base_repository import SqlAlchemyBaseRepository

from .mapper import RunsMapper
from .model import RunORM


class SqlAlchemyRunsRepository(
    SqlAlchemyBaseRepository[RunORM, Run,
                             RunWhere, RunFilter, RunsMapper],
    IRunsRepository,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, RunORM, RunsMapper)

    async def add(self, entity: Run) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._add(orm)

    async def get_unique(self, where: RunWhere) -> Run | None:
        return await super()._get_unique(where)

    async def list(self, filter: RunFilter | None = None, pagination: Pagination | None = None) -> PaginatedResponse[Run]:
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

    async def get_latest_version(self, parent_id: UUID) -> Run | None:
        where = RunWhere(id=parent_id, is_latest=True)
        return await self.get_unique(where)

    async def get_version_by_number(self, parent_id: UUID, version: int) -> Run | None:
        where = RunWhere(id=parent_id, version=version)
        return await self.get_unique(where)
