from uuid import UUID

from fastapi import APIRouter, Depends, status, File, UploadFile

from app.api.unit_of_work import get_uow
from app.features.datasets.guards import is_dataset_owner
from core.ports.unit_of_work import UnitOfWork

from .service import DatasetArtifactsService, get_dataset_artifacts_service

from ..guards.is_dataset_owner import is_dataset_owner
from ..dto.create_artifact import CreateArtifactDTO


dataset_artifacts_router = APIRouter(tags=["dataset_artifacts"])


@dataset_artifacts_router.post(
    path="/upload",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(is_dataset_owner)
    ]
)
async def upload_dataset_artifact(
    dataset_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
    file: UploadFile = File(...),
    dataset_artifacts_service: DatasetArtifactsService = Depends(
        get_dataset_artifacts_service),
):
    data = CreateArtifactDTO(dataset_id=dataset_id)
    return await dataset_artifacts_service.create(uow=uow, data=data, file=file.file)
