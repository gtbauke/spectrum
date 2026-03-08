from typing import Optional

from core.ports.unit_of_work import UnitOfWork
from core.services.base import BaseCRUDService

from core.models.datasets.dataset import Dataset
from core.models.datasets.where import DatasetsWhere, DatasetsFilter

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
    async def get_unique(self, *, uow: UnitOfWork, where: DatasetsWhere) -> Optional[Dataset]:
        return await uow.datasets.get_unique(where=where)

    async def create(self, *, uow: UnitOfWork, data: CreateDatasetDTO) -> Dataset:
        dataset = await uow.datasets.add(Dataset.new(
            name=data.name,
            description=data.description,
            owner_id=data.owner_id
        ))

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


def get_datasets_service() -> DatasetsService:
    return DatasetsService()
