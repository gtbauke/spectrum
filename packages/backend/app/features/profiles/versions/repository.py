from typing import Optional

from sqlalchemy import update, select, func

from app.core.repository import BaseRepositoryImplementation

from core.repositories.profiles import BaseProfileVersionsRepository
from core.models.profiles.profile_version import ProfileVersion
from core.models.profiles.where import ProfileVersionWhere, ProfileVersionFilter

from ..models import ProfileVersionORM


class ProfileVersionsRepository(BaseProfileVersionsRepository, BaseRepositoryImplementation[
    ProfileVersion,
    ProfileVersionORM,
    ProfileVersionWhere,
    ProfileVersionFilter
]):
    orm_model = ProfileVersionORM

    async def get_latest_version_number(self, where: ProfileVersionWhere) -> int:
        query = (
            select(func.max(self.orm_model.version))
            .where(where.resolve(self.orm_model))
        )

        result = await self._session.execute(query)
        scalar = result.scalar_one_or_none()

        if scalar is None:
            return 0

        return scalar

    async def unset_latest(self, where: ProfileVersionWhere) -> Optional[ProfileVersion]:
        query = (
            update(self.orm_model)
            .where(where.resolve(self.orm_model))
            .values(is_latest=False)
            .returning(self.orm_model)
        )

        result = await self._session.execute(query)
        obj_orm = result.scalar_one_or_none()

        return obj_orm.to_domain() if obj_orm else None
