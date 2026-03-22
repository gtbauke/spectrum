from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Sequence, Iterable

from core.features.profiles.jobs.repository import IJobsRepository
from core.features.profiles.jobs.job import Job
from core.features.profiles.jobs.where import JobWhere, JobFilter
from core.utils.pagination.base import Pagination
from core.utils.pagination.response import PaginatedResponse

from db.common.repositories.sql_alchemy_bulk_repository import SqlAlchemyBulkRepository

from .mapper import JobsMapper
from .model import JobORM


class SqlAlchemyJobsRepository(
    SqlAlchemyBulkRepository[JobORM, Job,
                             JobWhere, JobFilter, JobsMapper],
    IJobsRepository,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, JobORM, JobsMapper)

    async def add(self, entity: Job) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._add(entity=orm)

    async def update(self, entity: Job) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._update(entity=orm)

    async def delete(self, entity: Job) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._delete(entity=orm)

    async def add_many(self, entities: Iterable[Job]) -> None:
        orms = [self._mapper.to_orm(domain=entity) for entity in entities]
        await super()._add_many(entities=orms)

    async def update_many(self, entities: Iterable[Job]) -> None:
        orms = [self._mapper.to_orm(domain=entity) for entity in entities]
        await super()._update_many(entities=orms)

    async def delete_many(self, entities: Iterable[Job]) -> None:
        orms = [self._mapper.to_orm(domain=entity) for entity in entities]
        await super()._delete_many(entities=orms)

    async def get_unique(self, where: JobWhere) -> Job | None:
        query = (
            select(self._model_class)
            .options(
                selectinload(self._model_class.runs),
            )
            .where(*where.resolve(self._model_class))
        )

        result = await self._session.execute(statement=query)
        orm = result.scalar_one_or_none()

        if not orm:
            return None

        return self._mapper.to_domain(orm=orm)

    def _build_query(
        self,
        filter: JobFilter | None = None,
    ):
        resolved_filters = filter.resolve(
            self._model_class) if filter else None

        query = (
            select(self._model_class)
            .options(
                selectinload(self._model_class.runs),
            )
            .distinct()
        )

        if resolved_filters:
            query = query.where(*resolved_filters)

        return query

    async def list(
        self,
        filter: JobFilter | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[Job]:
        query = self._build_query(filter=filter)

        if pagination:
            query = query.limit(limit=pagination.limit).offset(
                offset=pagination.offset)

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
        filter: JobFilter | None = None,
    ) -> Sequence[Job]:
        query = self._build_query(filter=filter)
        return await self._list_all_query(query=query)
