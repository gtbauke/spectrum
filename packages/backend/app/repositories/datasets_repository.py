from typing import Optional

from uuid import UUID
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from app.db.models import DatasetORM

from core.models.datasets.dataset import Dataset
from core.repositories.datasets_repository import DatasetsRepository


class SqlAlchemyDatasetsRepository(DatasetsRepository):
    async def get_by_id(self, id: UUID) -> Dataset | None:
        result = await self._session.execute(
            select(DatasetORM)
            .where(DatasetORM.id == id)
            .options(
                selectinload(DatasetORM.jobs),
                selectinload(DatasetORM.models),
                selectinload(DatasetORM.dataset_metadata),
            )
        )

        dataset_orm = result.scalar_one_or_none()
        return dataset_orm.to_domain() if dataset_orm else None

    async def create(self, *, name: str) -> Dataset:
        dataset = DatasetORM(name=name)
        self._session.add(dataset)

        return dataset.to_domain()

    async def add(self, obj: Dataset) -> Dataset:
        self._session.add(DatasetORM.from_domain(obj))
        await self._session.flush()

        return obj

    async def update(self, obj: Dataset) -> Dataset:
        orm = DatasetORM.from_domain(obj)

        await self._session.merge(orm)
        await self._session.flush()

        return obj

    async def save(self, dataset: Dataset) -> None:
        await self._session.merge(DatasetORM.from_domain(dataset))

    async def get_for_update(self, id: UUID) -> Optional[Dataset]:
        statement = (
            select(DatasetORM)
            .where(DatasetORM.id == id)
            .with_for_update()
        )

        result = await self._session.execute(statement)
        orm = result.scalar_one_or_none()

        return orm.to_domain() if orm else None

    async def delete(self, id: UUID) -> None:
        await self._session.execute(
            delete(DatasetORM).where(DatasetORM.id == id)
        )

    async def list_all(self, where_id: Optional[UUID] = None) -> list[Dataset]:
        query = select(DatasetORM)
        if where_id:
            query = query.where(DatasetORM.id == where_id)

        result = await self._session.execute(query)

        return [obj.to_domain() for obj in result.scalars().all()]
