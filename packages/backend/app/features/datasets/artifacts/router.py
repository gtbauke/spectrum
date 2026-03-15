from uuid import UUID
from fastapi import APIRouter, Depends, status, File, UploadFile, Response

from app.api.unit_of_work import get_uow
from app.features.datasets.guards import is_dataset_owner

from core.ports.unit_of_work import UnitOfWork
from core.models.datasets.where import DatasetArtifactsFilter
from core.utils.filters.field_filter import UUIDFilter

from .service import DatasetArtifactsService, get_dataset_artifacts_service

from ..guards.is_dataset_owner import is_dataset_owner
from .dto.create_artifact import CreateArtifactDTO
from .dto.exists import DatasetArtifactExistsDTO


dataset_artifacts_router = APIRouter(tags=["dataset_artifacts"])


@dataset_artifacts_router.post(
    path="/check",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(is_dataset_owner)]
)
async def check_dataset_artifact_exists(
    dataset_id: UUID,
    checksum: str,
    uow: UnitOfWork = Depends(get_uow),
    dataset_artifacts_service: DatasetArtifactsService = Depends(
        get_dataset_artifacts_service),
):
    return await dataset_artifacts_service.already_exists(
        uow=uow,
        data=DatasetArtifactExistsDTO(dataset_id=dataset_id, checksum=checksum)
    )


@dataset_artifacts_router.post(
    path="/upload",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(is_dataset_owner)
    ]
)
async def upload_dataset_artifact(
    dataset_id: UUID,
    response: Response,
    uow: UnitOfWork = Depends(get_uow),
    file: UploadFile = File(...),
    dataset_artifacts_service: DatasetArtifactsService = Depends(
        get_dataset_artifacts_service),
):
    data = CreateArtifactDTO(dataset_id=dataset_id, dataset_version_id=None)
    res = await dataset_artifacts_service.create(uow=uow, data=data, file=file.file)

    if not res.was_created:
        response.status_code = status.HTTP_200_OK

    return res.artifact


@dataset_artifacts_router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(is_dataset_owner)
    ]
)
async def list_dataset_artifacts(
    dataset_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
    dataset_artifacts_service: DatasetArtifactsService = Depends(
        get_dataset_artifacts_service),
):
    return await dataset_artifacts_service.get_all(
        uow=uow,
        filter=DatasetArtifactsFilter(
            dataset_id=UUIDFilter(eq=dataset_id)
        )
    )
