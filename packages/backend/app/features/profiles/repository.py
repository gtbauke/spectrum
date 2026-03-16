from typing import Optional
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, joinedload

from app.api.response import RepositoryPaginatedResponse
from app.core.repository import BaseRepositoryImplementation

from app.features.owners.models import OwnerORM
from core.models.owners.owner_type import OwnerType
from core.repositories.profiles import BaseProfilesRepository
from core.models.profiles.profile import Profile
from core.models.profiles.where import ProfilesWhere, ProfileFilter
from core.utils.pagination.base import Pagination

from .models import ProfileDatasetAssociationORM, ProfileORM, ProfileVersionORM


class ProfilesRepository(BaseProfilesRepository, BaseRepositoryImplementation[
    Profile,
    ProfileORM,
    ProfilesWhere,
    ProfileFilter
]):
    orm_model = ProfileORM

    async def get_unique(self, where: ProfilesWhere) -> Optional[Profile]:
        query = (
            select(self.orm_model)
            .options(
                selectinload(self.orm_model.versions).options(
                    selectinload(ProfileVersionORM.datasets)
                    .selectinload(ProfileDatasetAssociationORM.dataset_version),

                    selectinload(ProfileVersionORM.blocks)
                )
            )
            .where(*where.resolve(self.orm_model))
        )

        result = await self._session.execute(query)
        obj_orm = result.scalar_one_or_none()

        return obj_orm.to_domain() if obj_orm else None

    async def get_owner_id(self, where: ProfilesWhere) -> Optional[UUID]:
        query = (
            select(self.orm_model.owner_id)
            .where(*where.resolve(self.orm_model))
        )

        result = await self._session.execute(query)
        scalar = result.scalar_one_or_none()

        return scalar

    async def list_all(self, where: ProfileFilter | None = None, pagination: Pagination | None = None) -> list[Profile]:
        query = (
            select(self.orm_model)
            .options(
                selectinload(self.orm_model.versions.and_(
                    ProfileVersionORM.is_latest == True)).options(
                    selectinload(ProfileVersionORM.datasets)
                    .selectinload(ProfileDatasetAssociationORM.dataset_version),

                    selectinload(ProfileVersionORM.blocks)
                )
            )
        )

        if where:
            conditions = where.resolve(self.orm_model)
            if len(conditions) > 0:
                query = query.where(*conditions)

        if pagination:
            query = pagination.apply(query)

        result = await self._session.execute(query)
        return [obj_orm.to_domain() for obj_orm in result.scalars().all()]

    async def get_paginated(self, *, filter: ProfileFilter, limit: int = 20, offset: int = 0) -> tuple[list[Profile], int]:
        conditions = filter.resolve(self.orm_model)

        count_query = select(func.count()).select_from(
            self.orm_model).where(*conditions)

        total = await self._session.execute(count_query)
        total_count = total.scalar_one() or 0

        query = (
            select(self.orm_model)
            .options(
                joinedload(
                    ProfileORM.owner.and_(
                        OwnerORM.owner_type == OwnerType.USER,
                    )
                ).options(
                    selectinload(OwnerORM.user),
                ),
                selectinload(self.orm_model.versions).options(
                    selectinload(ProfileVersionORM.datasets)
                    .selectinload(ProfileDatasetAssociationORM.dataset_version),

                    selectinload(ProfileVersionORM.blocks)
                )
            )
            .where(*conditions)
            .limit(limit)
            .offset(offset)
            .distinct()
        )

        result = await self._session.execute(query)
        obj_orms = result.scalars().all()

        return [obj_orm.to_domain() for obj_orm in obj_orms], total_count

    async def get_profiles_summary(self, *, filter: ProfileFilter, limit: int, offset: int):
        conditions = filter.resolve(self.orm_model)

        count_query = select(func.count()).select_from(
            self.orm_model).where(*conditions)

        total = await self._session.execute(count_query)
        total_count = total.scalar_one() or 0

        query = (
            select(ProfileORM)
            .options(
                joinedload(
                    ProfileORM.owner.and_(
                        OwnerORM.owner_type == OwnerType.USER,
                    )
                ).options(
                    selectinload(OwnerORM.user),
                ),
                selectinload(ProfileORM.versions).options(
                    selectinload(ProfileVersionORM.datasets)
                    .selectinload(ProfileDatasetAssociationORM.dataset_version),
                ),
            )
            .where(*conditions)
            .limit(limit)
            .offset(offset)
        )

        result = await self._session.execute(query)
        objs = result.scalars().all()
        items = [obj.to_domain() for obj in objs]

        return RepositoryPaginatedResponse(
            items=items,
            total=total_count,
        )
