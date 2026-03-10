from typing import Optional

from core.ports.unit_of_work import UnitOfWork
from core.services.base import BaseCRUDService

from core.models.datasets.dataset import Dataset
from core.models.datasets.where import DatasetsWhere, DatasetsFilter

from .versions.service import DatasetVersionsService, get_dataset_versions_service
from .versions.dto.create_version import CreateDatasetVersionDTO
from .dto.create_dataset import CreateDatasetDTO
from .dto.update_dataset import UpdateDatasetDTO
from .errors.dataset_not_found import DatasetNotFound


class DatasetsService(BaseCRUDService[
    Dataset,
    DatasetsWhere,
    CreateDatasetDTO,
    UpdateDatasetDTO,
    DatasetsFilter,
]):
    def __init__(
        self,
        versions_service: DatasetVersionsService,
    ):
        self._versions_service = versions_service

    async def get_unique_with_latest_version(
        self,
        *,
        uow: UnitOfWork,
        where: DatasetsWhere,
    ) -> Optional[Dataset]:
        return await uow.datasets.get_unique_with_latest_version(where=where)

    async def get_unique(self, *, uow: UnitOfWork, where: DatasetsWhere) -> Optional[Dataset]:
        return await uow.datasets.get_unique(where=where)

    async def create(self, *, uow: UnitOfWork, data: CreateDatasetDTO) -> Dataset:
        domain = Dataset.new(
            name=data.name,
            description=data.description,
            owner_id=data.owner_id
        )

        domain = await uow.datasets.add(domain)

        version = await self._versions_service.create(uow=uow, data=CreateDatasetVersionDTO(
            dataset_id=domain.id,
            version=1
        ))

        domain.add_version(version)
        dataset = await uow.datasets.update(domain)

        return dataset

    async def update_unique(self, *, uow: UnitOfWork, where: DatasetsWhere, data: UpdateDatasetDTO) -> Dataset:
        dataset = await uow.datasets.get_unique(where=where)

        if not dataset:
            raise DatasetNotFound(dataset_id=where.id)

        update_data = data.model_dump(exclude_unset=True)
        updated_dataset = dataset.model_copy(
            update=update_data
        )

        return await uow.datasets.update(updated_dataset)

    async def delete_unique(self, *, uow: UnitOfWork, where: DatasetsWhere):
        await uow.datasets.delete(where=where)

    async def get_all(self, *, uow: UnitOfWork, filter: Optional[DatasetsFilter] = None) -> list[Dataset]:
        return await uow.datasets.list_all(where=filter)

    async def get_paginated(self, *, uow: UnitOfWork, filter: DatasetsFilter, limit: int = 20, offset: int = 0) -> tuple[list[Dataset], int]:
        return await uow.datasets.get_paginated(filter=filter, limit=limit, offset=offset)


def get_datasets_service() -> DatasetsService:
    versions_service = get_dataset_versions_service()
    return DatasetsService(versions_service=versions_service)
