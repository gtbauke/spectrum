from abc import ABC, abstractmethod
from uuid import UUID

from app.repositories.base import BaseRepository
from app.db.models.dataset import DatasetMetadataORM


class DatasetsMetadataRepository(BaseRepository[DatasetMetadataORM], ABC):
    @abstractmethod
    async def create_or_get_for_update(
        self,
        dataset_id: UUID,
    ) -> DatasetMetadataORM: ...
