from typing import Optional
from abc import abstractmethod
from uuid import UUID

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
    @abstractmethod
    async def get_unique_with_latest_version(self, *, where: DatasetsWhere) -> Optional[Dataset]:
        ...

    @abstractmethod
    async def get_owner_id(self, *, where: DatasetsWhere) -> Optional[UUID]:
        ...


class BaseDatasetVersionsRepository(BaseRepository[DatasetVersion, DatasetVersionsWhere, DatasetVersionsFilter]):
    @abstractmethod
    async def unset_latest_version(self, *, where: DatasetVersionsWhere):
        ...


class BaseDatasetArtifactsRepository(BaseRepository[DatasetArtifact, DatasetArtifactsWhere, DatasetArtifactsFilter]):
    pass


class BaseDatasetArtifactVersionsRepository(BaseRepository[DatasetArtifactVersion, DatasetArtifactVersionsWhere, DatasetArtifactVersionsFilter]):
    pass
