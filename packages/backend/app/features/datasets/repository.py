from typing import Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.core.repository import BaseRepositoryImplementation

from .models import DatasetORM, DatasetVersionORM

from core.models.datasets.where import DatasetsFilter, DatasetsWhere
from core.models.datasets.dataset import Dataset
from core.repositories.datasets import BaseDatasetsRepository


class DatasetsRepository(BaseDatasetsRepository, BaseRepositoryImplementation[
    Dataset,
    DatasetORM,
    DatasetsWhere,
    DatasetsFilter
]):
    orm_model = DatasetORM

    async def get_unique(self, where: DatasetsWhere) -> Optional[Dataset]:
        query = (
            select(DatasetORM)
            .options(
                selectinload(DatasetORM.versions)
            )
            .where(where.resolve(DatasetORM))
        )

        result = await self._session.execute(query)
        obj_orm = result.scalar_one_or_none()

        return obj_orm.to_domain() if obj_orm else None

    async def get_unique_with_latest_version(self, *, where: DatasetsWhere) -> Optional[Dataset]:
        max_version_subquery = (
            select(func.max(DatasetVersionORM.version))
            .where(DatasetVersionORM.dataset_id == DatasetORM.id)
            .scalar_subquery()
        )

        query = (
            select(DatasetORM)
            .options(
                selectinload(DatasetORM.versions.and_(
                    DatasetVersionORM.version == max_version_subquery
                ))
            )
            .where(where.resolve(DatasetORM))
        )

        result = await self._session.execute(query)
        scalar = result.scalar_one_or_none()

        return scalar.to_domain() if scalar else None

    async def get_owner_id(self, *, where: DatasetsWhere) -> UUID | None:
        query = (
            select(DatasetORM.owner_id)
            .where(where.resolve(DatasetORM))
        )

        result = await self._session.execute(query)
        scalar = result.scalar_one_or_none()

        return scalar
