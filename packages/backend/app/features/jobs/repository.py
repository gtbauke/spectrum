from typing import Optional

from sqlalchemy import select, func, update, and_

from app.features.profiles.models import ProfileVersionORM
from app.features.profiles.service import ProfileVersionNotFound
from core.models.profiles.profile_version import ProfileVersion
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

    async def get_latest_version_number(self, where: JobWhere) -> int:
        query = (
            select(func.max(self.orm_model.version))
            .where(where.resolve(self.orm_model))
        )

        result = await self._session.execute(query)
        scalar = result.scalar_one_or_none()

        if scalar is None:
            return 0

        return scalar

    async def unset_latest(self, where: JobWhere) -> Optional[Job]:
        query = (
            update(self.orm_model)
            .where(where.resolve(self.orm_model))
            .values(is_latest=False)
            .returning(self.orm_model)
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
            .where(*conditions)
            .limit(limit)
            .offset(offset)
            .distinct()
        )

        result = await self._session.execute(query)
        obj_orms = result.scalars().all()

        return [obj_orm.to_domain() for obj_orm in obj_orms], total_count

    async def get_profile_version(self, *, where: JobWhere) -> ProfileVersion:
        query = (
            select(
                ProfileVersionORM
            )
            .join(
                ProfileVersionORM,
                and_(
                    self.orm_model.profile_version_id == ProfileVersionORM.id,
                    ProfileVersionORM.is_latest == True,
                )
            )
        )

        result = await self._session.execute(query)
        orm = result.scalar_one_or_none()

        if not orm:
            raise ProfileVersionNotFound()

        return orm.to_domain()
