from abc import ABC, abstractmethod
from uuid import UUID

from app.repositories.base import BaseRepository
from app.db.models.dataset import DatasetMetadataORM
from app.domain.datasets.dataset_metadata import DatasetMetadata


class DatasetsMetadataRepository(BaseRepository[DatasetMetadataORM, DatasetMetadata], ABC):
    @abstractmethod
    async def create_or_get_for_update(
        self,
        dataset_id: UUID,
    ) -> DatasetMetadataORM: ...
