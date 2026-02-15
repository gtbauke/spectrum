from typing import Optional
from uuid import UUID
from sqlalchemy import select

from app.db.models.job_run import JobRunORM
from app.repositories.job_run_repository import JobRunRepository


class SQLAlchemyJobRunRepository(JobRunRepository):
    async def get_by_id(self, id: UUID) -> Optional[JobRunORM]:
        return await self._session.get(JobRunORM, id)

    async def get_for_update(self, id: UUID) -> Optional[JobRunORM]:
        return await self._session.get(JobRunORM, id, with_for_update=True)

    async def add(self, obj: JobRunORM) -> JobRunORM:
        self._session.add(obj)
        await self._session.flush()
        return obj

    async def update(self, obj: JobRunORM) -> JobRunORM:
        await self._session.merge(obj)
        await self._session.flush()
        return obj

    async def delete(self, obj: JobRunORM) -> None:
        await self._session.delete(obj)
        await self._session.flush()

    async def list_all(self, where_id: Optional[UUID] = None) -> list[JobRunORM]:
        query = select(JobRunORM)
        if where_id:
            query = query.where(JobRunORM.model_id == where_id)

        result = await self._session.execute(query)
        return list(result.scalars().all())
