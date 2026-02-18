from abc import ABC, abstractmethod
from uuid import UUID

from core.models.datasets.dataset_metadata import DatasetMetadata
from core.repositories.base import BaseRepository


class DatasetsMetadataRepository(BaseRepository[DatasetMetadata], ABC):
    @abstractmethod
    async def create_or_get_for_update(
        self,
        dataset_id: UUID,
    ) -> DatasetMetadata: ...
