from typing import Optional

from core.ports.unit_of_work import UnitOfWork
from core.services.base import BaseCRDService

from core.models.datasets.dataset_version import DatasetVersion
from core.models.datasets.where import DatasetVersionsWhere, DatasetVersionsFilter

from ..artifact_version.service import DatasetArtifactVersionService
from .dto.associate_artifacts import AssociateArtifactsDTO
from .dto.create_version import CreateDatasetVersionDTO
from .errors.version_not_found import VersionNotFound


class DatasetVersionsService(BaseCRDService[
    DatasetVersion,
    DatasetVersionsWhere,
    CreateDatasetVersionDTO,
    DatasetVersionsFilter
]):
    def __init__(
        self,
        artifact_versions_service: DatasetArtifactVersionService,
    ):
        self._artifact_versions_service = artifact_versions_service

    async def get_unique(self, *, uow: UnitOfWork, where: DatasetVersionsWhere) -> Optional[DatasetVersion]:
        return await uow.dataset_versions.get_unique(where=where)

    async def create(self, *, uow: UnitOfWork, data: CreateDatasetVersionDTO) -> DatasetVersion:
        await uow.dataset_versions.unset_latest_version(where=DatasetVersionsWhere(dataset_id=data.dataset_id))

        return await uow.dataset_versions.add(DatasetVersion.new(
            dataset_id=data.dataset_id,
            version=data.version
        ))

    async def delete_unique(self, *, uow: UnitOfWork, where: DatasetVersionsWhere):
        await uow.dataset_versions.delete(where=where)

    async def get_all(self, *, uow: UnitOfWork, filter: Optional[DatasetVersionsFilter] = None) -> list[DatasetVersion]:
        return await uow.dataset_versions.list_all(where=filter)

    async def bulk_associate_artifacts(
        self,
        *,
        uow: UnitOfWork,
        where: DatasetVersionsWhere,
        data: AssociateArtifactsDTO,
    ):
        version = await uow.dataset_versions.get_unique(where=where)

        if not version:
            raise VersionNotFound()

        return await self._artifact_versions_service.create_bulk_association(
            uow=uow,
            dataset_version_id=version.id,
            data=data,
        )


def get_dataset_versions_service() -> DatasetVersionsService:
    artifact_versions_service = DatasetArtifactVersionService()
    return DatasetVersionsService(artifact_versions_service=artifact_versions_service)
