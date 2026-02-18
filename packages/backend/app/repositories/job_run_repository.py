from typing import Optional
from uuid import UUID
from sqlalchemy import delete, select

from app.db.models.job_run import JobRunORM

from core.models.jobs.job_run import JobRun
from core.repositories.job_run_repository import JobRunRepository


class SQLAlchemyJobRunRepository(JobRunRepository):
    async def get_by_id(self, id: UUID) -> Optional[JobRun]:
        orm = await self._session.get(JobRunORM, id)
        return orm.to_domain() if orm else None

    async def get_for_update(self, id: UUID) -> Optional[JobRun]:
        orm = await self._session.get(JobRunORM, id, with_for_update=True)
        return orm.to_domain() if orm else None

    async def add(self, obj: JobRun) -> JobRun:
        self._session.add(JobRunORM.from_domain(obj))
        await self._session.flush()

        return obj

    async def update(self, obj: JobRun) -> JobRun:
        await self._session.merge(JobRunORM.from_domain(obj))
        await self._session.flush()

        return obj

    async def delete(self, id: UUID) -> None:
        await self._session.execute(
            delete(JobRunORM).where(JobRunORM.id == id)
        )

    async def list_all(self, where_id: Optional[UUID] = None) -> list[JobRun]:
        query = select(JobRunORM)
        if where_id:
            query = query.where(JobRunORM.model_id == where_id)

        result = await self._session.execute(query)
        return [obj.to_domain() for obj in result.scalars().all()]
