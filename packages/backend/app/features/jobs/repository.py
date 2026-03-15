from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from core.repositories.jobs import BaseJobsRepository
from core.models.jobs.job import Job
from core.models.jobs.where import JobWhere, JobFilter

from app.core.repository import BaseRepositoryImplementation
from app.features.jobs.models import JobORM


class JobsRepository(BaseJobsRepository, BaseRepositoryImplementation[
    Job,
    JobORM,
    JobWhere,
    JobFilter,
]):
    orm_model = JobORM

    async def get_unique(self, where: JobWhere) -> Job | None:
        query = (
            select(self.orm_model)
            .options(
                selectinload(self.orm_model.versions),
            )
            .where(where.resolve(self.orm_model))
        )

        result = await self._session.execute(query)
        obj_orm = result.scalar_one_or_none()

        return obj_orm.to_domain() if obj_orm else None

    async def get_paginated(self, *, filter: JobFilter, limit: int = 20, offset: int = 0) -> tuple[list[Job], int]:
        conditions = filter.resolve(self.orm_model)

        count_query = select(func.count()).select_from(
            self.orm_model).where(*conditions)

        total = await self._session.execute(count_query)
        total_count = total.scalar_one() or 0

        query = (
            select(self.orm_model)
            .options(
                selectinload(self.orm_model.versions),
            )
            .where(*conditions)
            .limit(limit)
            .offset(offset)
            .distinct()
        )

        result = await self._session.execute(query)
        obj_orms = result.scalars().all()

        return [obj_orm.to_domain() for obj_orm in obj_orms], total_count
