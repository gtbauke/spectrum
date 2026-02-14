import logging

from typing import Optional
from uuid import UUID
from sqlalchemy import select

from app.repositories.jobs_repository import JobsRepository
from app.db.models.job import JobORM

logger = logging.getLogger(__name__)


class SQLAlchemyJobsRepository(JobsRepository):
    async def get_by_id(self, id: UUID) -> JobORM | None:
        result = await self._session.get(JobORM, id)
        return result

    async def get_for_update(self, id: UUID) -> JobORM | None:
        result = await self._session.execute(
            select(JobORM)
            .where(JobORM.id == id)
            .with_for_update()
        )

        return result.scalar_one_or_none()

    async def add(self, obj: JobORM) -> JobORM:
        self._session.add(obj)
        await self._session.flush()

        return obj

    async def update(self, obj: JobORM) -> JobORM:
        await self._session.merge(obj)
        return obj

    async def delete(self, obj: JobORM) -> None:
        await self._session.delete(obj)

    async def list_all(self, where_id: Optional[UUID] = None) -> list[JobORM]:
        query = select(JobORM)
        if where_id:
            query = query.where(JobORM.dataset_id == where_id)

        result = await self._session.execute(query)
        return list(result.scalars().all())
