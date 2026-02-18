from typing import Optional
from uuid import UUID
from sqlalchemy import delete, select

from app.db.models.dataset_metadata import DatasetMetadataORM
from core.models.datasets.dataset_metadata import DatasetMetadata
from core.repositories.datasets_metadata_repository import DatasetsMetadataRepository


class SqlAlchemyDatasetsMetadataRepository(DatasetsMetadataRepository):
    async def get_by_id(self, id: UUID) -> DatasetMetadata | None:
        result = await self._session.get(DatasetMetadataORM, id)
        return result.to_domain() if result else None

    async def get_for_update(self, id: UUID) -> Optional[DatasetMetadata]:
        raise NotImplementedError()

    async def add(self, obj: DatasetMetadata) -> DatasetMetadata:
        obj_orm = DatasetMetadataORM.from_domain(obj)

        self._session.add(obj_orm)
        await self._session.flush()

        return obj_orm.to_domain()

    async def create_or_get_for_update(
        self,
        dataset_id: UUID,
    ) -> DatasetMetadata:
        result = await self._session.execute(
            select(DatasetMetadataORM)
            .where(DatasetMetadataORM.dataset_id == dataset_id)
            .with_for_update()
        )

        metadata_orm = result.scalar_one_or_none()

        if metadata_orm:
            return metadata_orm.to_domain()

        metadata_orm = DatasetMetadataORM(
            dataset_id=dataset_id,
        )

        self._session.add(metadata_orm)
        await self._session.flush()

        return metadata_orm.to_domain()

    async def delete(self, id: UUID) -> None:
        await self._session.execute(
            delete(DatasetMetadataORM).where(DatasetMetadataORM.id == id)
        )

    async def update(self, obj: DatasetMetadata) -> DatasetMetadata:
        await self._session.merge(obj)
        await self._session.flush()

        return obj

    async def list_all(self, where_id: Optional[UUID] = None) -> list[DatasetMetadata]:
        query = select(DatasetMetadataORM)
        if where_id:
            query = query.where(DatasetMetadataORM.dataset_id == where_id)

        result = await self._session.execute(query)
        return [obj.to_domain() for obj in result.scalars().all()]
