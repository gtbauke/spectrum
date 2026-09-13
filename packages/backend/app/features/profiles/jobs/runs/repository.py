from datetime import datetime
from uuid import UUID
from typing import Protocol, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.ports.repositories.versioned import IVersionedRepository
from app.core.utils.pagination.base import Pagination
from app.core.utils.pagination.response import PaginatedResponse
from app.core.database.repositories.sql_alchemy_base_repository import SqlAlchemyBaseRepository

from app.features.profiles.jobs.runs.domain.status import JobRunStatus
from app.features.profiles.jobs.runs.domain.run import Run
from app.features.profiles.jobs.runs.domain.where import RunWhere, RunFilter
from .mapper import RunsMapper
from .model import RunORM


class IRunsRepository(IVersionedRepository[Run, RunWhere, RunFilter], Protocol):
    async def update_status(
        self,
        *,
        where: RunWhere,
        status: JobRunStatus,
        started_at: datetime | None = None,
        finished_at: datetime | None = None,
    ) -> Run | None: ...


class SqlAlchemyRunsRepository(
    SqlAlchemyBaseRepository[RunORM, Run,
                             RunWhere, RunFilter, RunsMapper],
    IRunsRepository,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, RunORM, RunsMapper)

    async def add(self, entity: Run) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._add(entity=orm)

    async def get_unique(self, where: RunWhere) -> Run | None:
        query = select(self._model_class).where(
            *where.resolve(self._model_class))

        result = await self._session.execute(query)
        orm = result.scalars().first()

        return self._mapper.to_domain(orm) if orm else None

    def _build_query(
        self,
        filter: RunFilter | None = None,
    ):
        resolved_filters = filter.resolve(
            self._model_class) if filter else None

        query = select(self._model_class).distinct()

        if resolved_filters:
            query = query.where(*resolved_filters)

        return query

    async def list(
        self,
        filter: RunFilter | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[Run]:
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
        filter: RunFilter | None = None,
    ) -> Sequence[Run]:
        query = self._build_query(filter=filter)
        return await self._list_all_query(query=query)

    async def get_latest_version(self, parent_id: UUID) -> Run | None:
        where = RunWhere(job_id=parent_id, is_latest=True)
        return await self.get_unique(where=where)

    async def get_version_by_number(self, parent_id: UUID, version: int) -> Run | None:
        where = RunWhere(job_id=parent_id, version=version)
        return await self.get_unique(where=where)

    async def unset_latest_and_add(self, parent_id: UUID, new_entity: Run) -> None:
        latest = await self.get_latest_version(parent_id=parent_id)

        if latest:
            latest_updated = latest.model_copy(update={"is_latest": False})
            mapped_orm = self._mapper.to_orm(domain=latest_updated)
            await super()._update(entity=mapped_orm)

        await self.add(entity=new_entity)

    async def update_status(
        self,
        *,
        where: RunWhere,
        status: JobRunStatus,
        started_at: datetime | None = None,
        finished_at: datetime | None = None,
    ) -> Run | None:
        run = await self.get_unique(where=where)

        if not run:
            return None

        updates: dict[str, object] = {"status": status}
        if started_at is not None:
            updates["started_at"] = started_at
        if finished_at is not None:
            updates["finished_at"] = finished_at

        updated_run = run.model_copy(update=updates)
        mapped_orm = self._mapper.to_orm(domain=updated_run)
        await super()._update(entity=mapped_orm)

        return updated_run
