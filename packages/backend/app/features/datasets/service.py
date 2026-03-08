import pandas as pd

from typing import Optional, BinaryIO

from core.ports.unit_of_work import UnitOfWork
from core.services.base import BaseService

from core.models.datasets.dataset import Dataset
from core.models.datasets.dataset_version import DatasetVersion
from core.models.datasets.dataset_artifact import DatasetArtifact
from core.models.datasets.artifact_type import ArtifactType
from core.models.datasets.where import DatasetsWhere, DatasetsFilter

from .dto.create_dataset import CreateDatasetDTO
from .dto.update_dataset import UpdateDatasetDTO
from .results.create_dataset import CreateDatasetResult
from .errors.dataset_not_found import DatasetNotFound


class DatasetsService(BaseService):
    async def get_unique(self, *, uow: UnitOfWork, where: DatasetsWhere) -> Optional[Dataset]:
        return await uow.datasets.get_unique(where=where)

    # TODO: check if user uploaded CSV file
    async def create(self, *, uow: UnitOfWork, data: CreateDatasetDTO, file: BinaryIO) -> CreateDatasetResult:
        dataset = await uow.datasets.add(Dataset.new(
            name=data.name,
            description=data.description,
            owner_id=data.owner_id
        ))

        df = pd.read_csv(file)

        row_count = len(df)
        column_count = len(df.columns)

        dataset_version = await uow.dataset_versions.add(DatasetVersion.new(
            dataset_id=dataset.id,
            row_count=row_count,
            column_count=column_count,
        ))

        storage_path = f"datasets/{dataset.id}/v{dataset_version.version}/data.csv"
        result = await uow.file_storage.upload(
            path=storage_path,
            file=file,
        )

        dataset_artifact = await uow.dataset_artifacts.add(DatasetArtifact.new(
            dataset_version_id=dataset_version.id,
            artifact_type=ArtifactType.DATA,
            file_path=storage_path,
            size_in_bytes=result.size,
            checksum=result.checksum,
        ))

        return CreateDatasetResult(
            dataset=dataset,
            dataset_version=dataset_version,
            dataset_artifact=dataset_artifact,
        )

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
