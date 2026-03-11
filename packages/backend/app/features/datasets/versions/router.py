from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.unit_of_work import get_uow
from core.ports.unit_of_work import UnitOfWork
from core.models.datasets.where import DatasetVersionsWhere

from ..guards.is_dataset_owner import is_dataset_owner
from .dto.associate_artifacts import AssociateArtifactsDTO, AssociateArtifactsRouteDTO
from .service import get_dataset_versions_service, DatasetVersionsService

dataset_versions_router = APIRouter(
    tags=["dataset_versions"],
    dependencies=[Depends(is_dataset_owner)]
)


@dataset_versions_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
)
async def create_version(
    dataset_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
    versions_service: DatasetVersionsService = Depends(
        get_dataset_versions_service),
):
    return await versions_service.create_new_version(
        dataset_id=dataset_id,
        uow=uow,
    )


@dataset_versions_router.post(
    path="/{version}/artifacts",
    status_code=status.HTTP_201_CREATED,
)
async def associate_artifacts_with_version(
    dataset_id: UUID,
    version: int,
    data: AssociateArtifactsRouteDTO,
    uow: UnitOfWork = Depends(get_uow),
    versions_service: DatasetVersionsService = Depends(
        get_dataset_versions_service),
):
    return await versions_service.bulk_associate_artifacts(
        where=DatasetVersionsWhere(version=version),
        data=AssociateArtifactsDTO(
            associations=data.associations,
            dataset_id=dataset_id,
        ),
        uow=uow,
    )
