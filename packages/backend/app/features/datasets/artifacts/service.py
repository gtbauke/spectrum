from typing import Optional, BinaryIO
from pydantic import BaseModel

from core.models.datasets.artifact_type import ArtifactType
from core.models.datasets.dataset_artifact_version import DatasetArtifactVersion
from core.ports.unit_of_work import UnitOfWork
from core.services.base import BaseService

from core.models.datasets.dataset_artifact import DatasetArtifact
from core.models.datasets.where import DatasetArtifactsWhere, DatasetArtifactsFilter

from .dto.create_artifact import CreateArtifactDTO
from .dto.exists import DatasetArtifactExistsDTO
from ..utils.checksum import checksum_and_size


class DatasetArtifactCreateResponse(BaseModel):
    artifact: DatasetArtifact
    association: Optional[DatasetArtifactVersion]

    was_created: bool


class DatasetArtifactsService(BaseService):
    async def get_unique(self, *, uow: UnitOfWork, where: DatasetArtifactsWhere) -> Optional[DatasetArtifact]:
        return await uow.dataset_artifacts.get_unique(where=where)

    async def create(self, *, uow: UnitOfWork, data: CreateArtifactDTO, file: BinaryIO) -> DatasetArtifactCreateResponse:
        checksum, size = await checksum_and_size(file)

        existing = await uow.dataset_artifacts.get_unique(
            where=DatasetArtifactsWhere(
                dataset_id=data.dataset_id, checksum=checksum)
        )

        if existing:
            return DatasetArtifactCreateResponse(
                artifact=existing,
                was_created=False,
                association=None,
            )

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

        association = None
        if data.dataset_version_id:
            association = DatasetArtifactVersion.new(
                artifact_type=ArtifactType.DATA,
                dataset_artifact_id=artifact.id,
                dataset_artifact=artifact,
                dataset_version_id=data.dataset_version_id,
            )

            association = await uow.dataset_artifact_versions.add(association)

        if association is None:
            artifact = await uow.dataset_artifacts.add(artifact)

        return DatasetArtifactCreateResponse(
            artifact=artifact,
            was_created=True,
            association=association
        )

    async def delete_unique(self, *, uow: UnitOfWork, where: DatasetArtifactsWhere):
        await uow.dataset_artifacts.delete(where=where)

    async def get_all(self, *, uow: UnitOfWork, filter: Optional[DatasetArtifactsFilter] = None) -> list[DatasetArtifact]:
        return await uow.dataset_artifacts.list_all(where=filter)

    async def already_exists(self, *, uow: UnitOfWork, data: DatasetArtifactExistsDTO) -> bool:
        existing = await uow.dataset_artifacts.get_unique(
            where=DatasetArtifactsWhere(
                dataset_id=data.dataset_id, checksum=data.checksum)
        )

        return existing is not None


def get_dataset_artifacts_service() -> DatasetArtifactsService:
    return DatasetArtifactsService()
