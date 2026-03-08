from sqlalchemy import select, update
from typing import Optional
from datetime import datetime, timezone


from .models import DatasetORM

from core.models.datasets.where import DatasetsFilter, DatasetsWhere
from core.models.datasets.dataset import Dataset
from core.repositories.datasets import BaseDatasetsRepository
from core.utils.pagination.base import Pagination


class DatasetsRepository(BaseDatasetsRepository):
    async def get_unique(self, where: DatasetsWhere) -> Optional[Dataset]:
        query = select(DatasetORM).where(where.resolve(DatasetORM))
        result = await self._session.execute(query)

        dataset_orm = result.scalar_one_or_none()
        return dataset_orm.to_domain() if dataset_orm else None

    async def get_for_update(self, where: DatasetsWhere) -> Dataset | None:
        query = select(DatasetORM).where(
            where.resolve(DatasetORM)).with_for_update()
        result = await self._session.execute(query)

        dataset_orm = result.scalar_one_or_none()
        return dataset_orm.to_domain() if dataset_orm else None

    async def add(self, obj: Dataset) -> Dataset:
        self._session.add(DatasetORM.from_domain(obj))

        await self._session.commit()
        return obj

    async def update(self, obj: Dataset) -> Dataset:
        await self._session.merge(DatasetORM.from_domain(obj))
        await self._session.commit()

        return obj

    async def delete(self, where: DatasetsWhere) -> None:
        query = update(DatasetORM).where(
            where.resolve(DatasetORM)).values(deleted_at=datetime.now(timezone.utc))

        await self._session.execute(query)
        await self._session.commit()

    async def list_all(self, where: Optional[DatasetsFilter] = None,
                       pagination: Optional[Pagination] = None) -> list[Dataset]:
        statement = select(DatasetORM)

        if where:
            conditions = where.resolve(DatasetORM)
            if len(conditions) > 0:
                statement = statement.where(*conditions)

        if pagination:
            statement = pagination.apply(statement)

        result = await self._session.execute(statement)

        return [dataset_orm.to_domain() for dataset_orm in result.scalars().all()]
