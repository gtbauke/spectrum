from uuid import UUID
from typing import Sequence

from app.core.ports.unit_of_work import UnitOfWork
from app.core.utils.pagination.base import Pagination
from app.core.utils.pagination.response import PaginatedResponse
from app.features.datasets.domain.dataset import Dataset
from app.features.datasets.domain.artifact import Artifact
from app.features.datasets.domain.where import (
    DatasetWhere,
    DatasetFilter,
    ArtifactWhere,
)
from app.features.datasets.errors.dataset_not_found import DatasetNotFound
from app.features.datasets.errors.artifact_not_found import ArtifactNotFound


class DatasetsService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def get_dataset_by_id(self, dataset_id: UUID) -> Dataset:
        dataset = await self._uow.datasets.get_unique(DatasetWhere(id=dataset_id))
        if not dataset:
            raise DatasetNotFound()
        return dataset

    async def get_artifact_by_id(self, artifact_id: UUID) -> Artifact:
        artifact = await self._uow.artifacts.get_unique(ArtifactWhere(id=artifact_id))
        if not artifact:
            raise ArtifactNotFound()
        return artifact

    async def list_datasets(
        self,
        filter: DatasetFilter | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[Dataset]:
        return await self._uow.datasets.list(filter=filter, pagination=pagination)

    async def list_all_datasets(
        self,
        filter: DatasetFilter | None = None,
    ) -> Sequence[Dataset]:
        return await self._uow.datasets.list_all(filter=filter)
