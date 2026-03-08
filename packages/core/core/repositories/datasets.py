from .base import BaseRepository

from core.models.datasets.dataset import Dataset
from core.models.datasets.dataset_version import DatasetVersion
from core.models.datasets.dataset_artifact import DatasetArtifact
from core.models.datasets.dataset_artifact_version import DatasetArtifactVersion
from core.models.datasets.where import (
    DatasetsWhere,
    DatasetsFilter,
    DatasetVersionsWhere,
    DatasetVersionsFilter,
    DatasetArtifactsWhere,
    DatasetArtifactsFilter,
    DatasetArtifactVersionsWhere,
    DatasetArtifactVersionsFilter,
)


class BaseDatasetsRepository(BaseRepository[Dataset, DatasetsWhere, DatasetsFilter]):
    pass


class BaseDatasetVersionsRepository(BaseRepository[DatasetVersion, DatasetVersionsWhere, DatasetVersionsFilter]):
    pass


class BaseDatasetArtifactsRepository(BaseRepository[DatasetArtifact, DatasetArtifactsWhere, DatasetArtifactsFilter]):
    pass


class BaseDatasetArtifactVersionsRepository(BaseRepository[DatasetArtifactVersion, DatasetArtifactVersionsWhere, DatasetArtifactVersionsFilter]):
    pass
