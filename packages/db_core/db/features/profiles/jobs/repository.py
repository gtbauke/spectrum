from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.features.profiles.jobs.repository import IJobsRepository
from core.features.profiles.jobs.job import Job
from core.features.profiles.jobs.where import JobWhere, JobFilter
from core.utils.pagination.base import Pagination
from core.utils.pagination.response import PaginatedResponse

from db.common.repositories.sql_alchemy_base_repository import SqlAlchemyBaseRepository

from .mapper import JobsMapper
from .model import JobORM


class SqlAlchemyJobsRepository(
    SqlAlchemyBaseRepository[JobORM, Job,
                             JobWhere, JobFilter, JobsMapper],
    IJobsRepository,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, JobORM, JobsMapper)

    async def add(self, entity: Job) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._add(orm)

    async def update(self, entity: Job) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._update(orm)

    async def delete(self, entity: Job) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._delete(orm)

    async def get_unique(self, where: JobWhere) -> Job | None:
        return await super()._get_unique(where)

    async def list(self, filter: JobFilter | None = None, pagination: Pagination | None = None) -> PaginatedResponse[Job]:
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
