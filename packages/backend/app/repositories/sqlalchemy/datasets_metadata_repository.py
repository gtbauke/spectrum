from typing import Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.datasets_metadata_repository import DatasetsMetadataRepository
from app.db.models.dataset import DatasetMetadataORM


class SqlAlchemyDatasetsMetadataRepository(DatasetsMetadataRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    async def get_by_id(self, id: UUID) -> DatasetMetadataORM | None:
        result = await self._session.execute(
            select(DatasetMetadataORM).where(DatasetMetadataORM.id == id)
        )

        return result.scalar_one_or_none()

    async def get_for_update(self, id: UUID) -> Optional[DatasetMetadataORM]:
        raise NotImplementedError()

    async def add(self, obj: DatasetMetadataORM) -> DatasetMetadataORM:
        self._session.add(obj)
        await self._session.flush()

        return obj
