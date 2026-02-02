from typing import Optional

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import DatasetORM
from app.domain.datasets.dataset import Dataset
from app.repositories.datasets_repository import DatasetsRepository


class SqlAlchemyDatasetsRepository(DatasetsRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    async def get(self, dataset_id: UUID) -> DatasetORM | None:
        result = await self._session.execute(
            select(DatasetORM).where(DatasetORM.id == dataset_id)
        )

        return result.scalar_one_or_none()

    async def create(self, *, name: str) -> DatasetORM:
        dataset = DatasetORM(name=name)
        self._session.add(dataset)

        return dataset

    async def add(self, dataset: DatasetORM) -> DatasetORM:
        self._session.add(dataset)
        await self._session.flush()

        return dataset

    async def update(self, dataset: DatasetORM) -> None:
        await self._session.merge(dataset)

    async def save(self, dataset: Dataset) -> None:
        await self._session.merge(DatasetORM.from_domain(dataset))

    async def get_for_update(self, dataset_id: UUID) -> Optional[Dataset]:
        statement = (
            select(DatasetORM)
            .where(DatasetORM.id == dataset_id)
            .with_for_update()
        )

        result = await self._session.execute(statement)
        orm = result.scalar_one_or_none()

        return orm.to_domain() if orm else None
