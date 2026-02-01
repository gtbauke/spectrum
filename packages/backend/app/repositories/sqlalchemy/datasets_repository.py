from app.repositories.datasets_repository import DatasetsRepository

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import DatasetORM


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
