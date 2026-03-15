from typing import Optional

from sqlalchemy import select, func, update, and_

from app.features.profiles.models import ProfileVersionORM
from app.features.profiles.service import ProfileVersionNotFound
from core.models.profiles.profile_version import ProfileVersion
from core.repositories.jobs import BaseJobVersionsRepository
from core.models.jobs.job_version import JobVersion
from core.models.jobs.where import JobVersionWhere, JobVersionFilter

from app.core.repository import BaseRepositoryImplementation
from app.features.jobs.models import JobORM, JobVersionORM


class JobVersionsRepository(BaseJobVersionsRepository, BaseRepositoryImplementation[
    JobVersion,
    JobVersionORM,
    JobVersionWhere,
    JobVersionFilter,
]):
    orm_model = JobVersionORM

    async def get_latest_version_number(self, where: JobVersionWhere) -> int:
        query = (
            select(func.max(self.orm_model.version))
            .where(where.resolve(self.orm_model))
        )

        result = await self._session.execute(query)
        scalar = result.scalar_one_or_none()

        if scalar is None:
            return 0

        return scalar

    async def unset_latest(self, where: JobVersionWhere) -> Optional[JobVersion]:
        query = (
            update(self.orm_model)
            .where(where.resolve(self.orm_model))
            .values(is_latest=False)
            .returning(self.orm_model)
        )

        result = await self._session.execute(query)
        obj_orm = result.scalar_one_or_none()

        return obj_orm.to_domain() if obj_orm else None

    async def get_paginated(self, *, filter: JobVersionFilter, limit: int = 20, offset: int = 0) -> tuple[list[JobVersion], int]:
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

    async def get_profile_version(self, *, where: JobVersionWhere) -> ProfileVersion:
        query = (
            select(
                ProfileVersionORM,
            )
            .join(
                JobORM,
                self.orm_model.job_id == JobORM.id,
            ).join(
                ProfileVersionORM,
                and_(
                    ProfileVersionORM.id == JobORM.profile_version_id,
                    ProfileVersionORM.is_latest == True,
                ),
            )
        )

        result = await self._session.execute(query)
        orm = result.scalar_one_or_none()

        if not orm:
            raise ProfileVersionNotFound()

        return orm.to_domain()
