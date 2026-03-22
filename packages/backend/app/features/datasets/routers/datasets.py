from uuid import UUID
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status, UploadFile, File, Form, Query

from app.api.unit_of_work import get_uow
from app.features.datasets.errors.dataset_not_found import DatasetNotFound
from app.features.datasets.guards import can_edit_dataset

from app.features.auth.guards.get_current_user import get_current_user
from app.features.datasets.guards.can_edit_dataset import can_edit_dataset

from core.ports.unit_of_work import UnitOfWork
from core.features.datasets.dataset import Dataset
from core.features.datasets.artifact import Artifact
from core.features.datasets.artifact_role import ArtifactRole
from core.features.datasets.where import DatasetWhere, DatasetFilter
from core.utils.pagination.base import Pagination
from core.utils.filters.field_filter import UUIDFilter

from .artifacts import artifacts_router

datasets_router = APIRouter()

datasets_router.include_router(
    artifacts_router, prefix="/{dataset_id}/artifacts", tags=["Dataset Artifacts"])


@datasets_router.post(
    path="/upload", response_model=Dataset, status_code=status.HTTP_201_CREATED)
async def upload_dataset(
    name: str = Form(...),
    description: str = Form(""),
    file: UploadFile = File(...),
    current_user_id: UUID = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    dataset = Dataset.new(
        name=name,
        description=description,
        owner_id=current_user_id
    )

    await uow.datasets.add(dataset)

    path = f"/datasets/{dataset.id}/artifacts/{file.filename}"
    upload_result = await uow.file_storage.upload(path=path, file=file.file)

    artifact = Artifact(
        dataset_id=dataset.id,
        checksum=upload_result.checksum,
        size_in_bytes=upload_result.size,
        path=upload_result.path,
        role=ArtifactRole.DATA
    )

    await uow.artifacts.add(artifact)
    dataset.artifacts.append(artifact)

    return dataset


@datasets_router.get(
    path="",
    response_model=None,
)
async def list_datasets(
    limit: int = Query(50, ge=1),
    offset: int = Query(0, ge=0),
    mine: bool = Query(
        False, description="Filter datasets owned by the current user"),
    current_user_id: UUID = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    pagination = Pagination(limit=limit, offset=offset)

    dataset_filter = None
    if mine:
        dataset_filter = DatasetFilter(owner_id=UUIDFilter(eq=current_user_id))

    paginated_response = await uow.datasets.list(filter=dataset_filter, pagination=pagination)
    return paginated_response


@datasets_router.get(
    path="/{dataset_id}",
    response_model=Dataset,
    dependencies=[
        Depends(get_current_user)
    ]
)
async def get_dataset(
    dataset_id: UUID,
    uow: UnitOfWork = Depends(get_uow)
):
    dataset = await uow.datasets.get_unique(DatasetWhere(id=dataset_id))

    if not dataset:
        raise DatasetNotFound()

    return dataset


@datasets_router.delete(
    path="/{dataset_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(can_edit_dataset)
    ]
)
async def delete_dataset(
    dataset_id: UUID,
    uow: UnitOfWork = Depends(get_uow)
):
    dataset = await uow.datasets.get_unique(DatasetWhere(id=dataset_id))

    if not dataset:
        raise DatasetNotFound()

    dataset.deleted_at = datetime.now(tz=timezone.utc)
    await uow.datasets.update(dataset)

    return None
