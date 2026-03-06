from .base import BaseRepository

from core.models.datasets.dataset import Dataset
from core.models.datasets.dataset_version import DatasetVersion
from core.models.datasets.dataset_artifact import DatasetArtifact
from core.models.datasets.where import (
    DatasetsWhere,
    DatasetVersionsWhere,
    DatasetArtifactsWhere
)


class BaseDatasetsRepository(BaseRepository[Dataset, DatasetsWhere]):
    pass


class BaseDatasetVersionsRepository(BaseRepository[DatasetVersion, DatasetVersionsWhere]):
    pass


class BaseDatasetArtifactsRepository(BaseRepository[DatasetArtifact, DatasetArtifactsWhere]):
    pass
