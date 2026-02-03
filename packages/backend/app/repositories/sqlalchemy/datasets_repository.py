from typing import Optional

from uuid import UUID
from sqlalchemy import select

from app.db.models import DatasetORM
from app.domain.datasets.dataset import Dataset
from app.repositories.datasets_repository import DatasetsRepository


class SqlAlchemyDatasetsRepository(DatasetsRepository):
    async def get_by_id(self, id: UUID) -> DatasetORM | None:
        result = await self._session.execute(
            select(DatasetORM).where(DatasetORM.id == id)
        )

        return result.scalar_one_or_none()

    async def create(self, *, name: str) -> DatasetORM:
        dataset = DatasetORM(name=name)
        self._session.add(dataset)

        return dataset

    async def add(self, obj: DatasetORM) -> DatasetORM:
        self._session.add(obj)
        await self._session.flush()

        return obj

    async def update(self, dataset: DatasetORM) -> None:
        await self._session.merge(dataset)

    async def save(self, dataset: Dataset) -> None:
        await self._session.merge(DatasetORM.from_domain(dataset))

    async def get_for_update(self, id: UUID) -> Optional[DatasetORM]:
        statement = (
            select(DatasetORM)
            .where(DatasetORM.id == id)
            .with_for_update()
        )

        result = await self._session.execute(statement)
        orm = result.scalar_one_or_none()

        return orm
