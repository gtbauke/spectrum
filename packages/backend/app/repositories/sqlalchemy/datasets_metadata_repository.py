from typing import Optional
from uuid import UUID
from sqlalchemy import select

from app.repositories.datasets_metadata_repository import DatasetsMetadataRepository
from app.db.models.dataset import DatasetMetadataORM


class SqlAlchemyDatasetsMetadataRepository(DatasetsMetadataRepository):
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

    async def create_or_get_for_update(
        self,
        dataset_id: UUID,
    ) -> DatasetMetadataORM:
        result = await self._session.execute(
            select(DatasetMetadataORM)
            .where(DatasetMetadataORM.dataset_id == dataset_id)
            .with_for_update()
        )

        metadata_orm = result.scalar_one_or_none()

        if metadata_orm:
            return metadata_orm

        metadata_orm = DatasetMetadataORM(
            dataset_id=dataset_id,
        )

        self._session.add(metadata_orm)
        await self._session.flush()

        return metadata_orm

    async def delete(self, obj: DatasetMetadataORM) -> None:
        await self._session.delete(obj)

    async def update(self, obj: DatasetMetadataORM) -> DatasetMetadataORM:
        await self._session.merge(obj)
        return obj

    async def list_all(self, where_id: Optional[UUID] = None) -> list[DatasetMetadataORM]:
        query = select(DatasetMetadataORM)
        if where_id:
            query = query.where(DatasetMetadataORM.dataset_id == where_id)

        result = await self._session.execute(query)
        return list(result.scalars().all())
