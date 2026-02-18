import logging

from typing import Optional
from uuid import UUID
from sqlalchemy import delete, select

from app.db.models.job import JobORM

from core.models.jobs.job import Job
from core.repositories.jobs_repository import JobsRepository

logger = logging.getLogger(__name__)


class SQLAlchemyJobsRepository(JobsRepository):
    async def get_by_id(self, id: UUID) -> Job | None:
        result = await self._session.get(JobORM, id)
        return result.to_domain() if result else None

    async def get_for_update(self, id: UUID) -> Job | None:
        result = await self._session.execute(
            select(JobORM)
            .where(JobORM.id == id)
            .with_for_update()
        )

        obj = result.scalar_one_or_none()
        return obj.to_domain() if obj else None

    async def add(self, obj: Job) -> Job:
        self._session.add(JobORM.from_domain(obj))
        await self._session.flush()

        return obj

    async def update(self, obj: Job) -> Job:
        await self._session.merge(JobORM.from_domain(obj))
        return obj

    async def delete(self, id: UUID) -> None:
        await self._session.execute(
            delete(JobORM).where(JobORM.id == id)
        )

    async def list_all(self, where_id: Optional[UUID] = None) -> list[Job]:
        query = select(JobORM)
        if where_id:
            query = query.where(JobORM.dataset_id == where_id)

        result = await self._session.execute(query)
        return [obj.to_domain() for obj in result.scalars().all()]
