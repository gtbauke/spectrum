from typing import Optional, BinaryIO

from core.ports.unit_of_work import UnitOfWork
from core.services.base import BaseService

from core.models.datasets.dataset_artifact import DatasetArtifact
from core.models.datasets.where import DatasetArtifactsWhere, DatasetArtifactsFilter

from .dto.create_artifact import CreateArtifactDTO
from ..utils.checksum import checksum_and_size


class DatasetArtifactsService(BaseService):
    async def get_unique(self, *, uow: UnitOfWork, where: DatasetArtifactsWhere) -> Optional[DatasetArtifact]:
        return await uow.dataset_artifacts.get_unique(where=where)

    async def create(self, *, uow: UnitOfWork, data: CreateArtifactDTO, file: BinaryIO) -> DatasetArtifact:
        checksum, size = await checksum_and_size(file)
        file_path = f"datasets/{data.dataset_id}/artifacts/{checksum}"

        await uow.file_storage.upload(
            file=file,
            path=file_path
        )

        artifact = DatasetArtifact.new(
            checksum=checksum,
            size_in_bytes=size,
            dataset_id=data.dataset_id,
            file_path=file_path,
        )

        return await uow.dataset_artifacts.add(artifact)

    async def delete_unique(self, *, uow: UnitOfWork, where: DatasetArtifactsWhere):
        await uow.dataset_artifacts.delete(where=where)

    async def get_all(self, *, uow: UnitOfWork, filter: Optional[DatasetArtifactsFilter] = None) -> list[DatasetArtifact]:
        return await uow.dataset_artifacts.list_all(where=filter)


def get_dataset_artifacts_service() -> DatasetArtifactsService:
    return DatasetArtifactsService()
