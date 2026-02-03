from abc import ABC

from app.repositories.base import BaseRepository
from app.db.models.dataset import DatasetMetadataORM
from app.domain.datasets.dataset_metadata import DatasetMetadata


class DatasetsMetadataRepository(BaseRepository[DatasetMetadataORM, DatasetMetadata], ABC):
    pass
