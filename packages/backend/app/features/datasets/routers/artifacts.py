from uuid import UUID
from fastapi import APIRouter, Depends, status, UploadFile, File, Form, Query
import tempfile
import pandas as pd
from typing import Any
from fastapi.concurrency import run_in_threadpool

from app.api.unit_of_work import get_uow
from app.features.datasets.errors.artifact_not_found import ArtifactNotFound


from app.features.auth.guards.get_current_user import get_current_user
from app.features.datasets.guards.can_edit_dataset import can_edit_dataset

from core.ports.unit_of_work import UnitOfWork
from core.features.datasets.artifact import Artifact
from core.features.datasets.artifact_role import ArtifactRole
from core.features.datasets.where import ArtifactWhere, ArtifactFilter
from core.utils.filters.field_filter import UUIDFilter

artifacts_router = APIRouter()


@artifacts_router.post(
    path="",
    response_model=Artifact,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(can_edit_dataset),
    ]
)
async def upload_artifact(
    dataset_id: UUID,
    file: UploadFile = File(...),
    role: ArtifactRole = Form(...),
    group_by_columns: str = Form(""),
    uow: UnitOfWork = Depends(get_uow)
):
    path = f"datasets/{dataset_id}/artifacts/{file.filename}"
    upload_result = await uow.file_storage.upload(path=path, file=file.file)

    artifact = Artifact(
        dataset_id=dataset_id,
        checksum=upload_result.checksum,
        size_in_bytes=upload_result.size,
        path=upload_result.path,
        role=role,
        group_by_columns=group_by_columns.replace("[", "").replace("]", "").replace("\"", "").split(
            ",") if group_by_columns else [],
    )

    await uow.artifacts.add(artifact)
    return artifact


@artifacts_router.get(
    path="",
    dependencies=[
        Depends(get_current_user),
    ]
)
async def list_artifacts(
    dataset_id: UUID,
    uow: UnitOfWork = Depends(get_uow)
):
    artifact_filter = ArtifactFilter(dataset_id=UUIDFilter(eq=dataset_id))
    paginated_response = await uow.artifacts.list(filter=artifact_filter, pagination=None)
    return paginated_response


@artifacts_router.get(
    path="/{artifact_id}",
    response_model=Artifact,
    dependencies=[
        Depends(get_current_user),
    ]
)
async def get_artifact(
    dataset_id: UUID,
    artifact_id: UUID,
    uow: UnitOfWork = Depends(get_uow)
):
    artifact = await uow.artifacts.get_unique(ArtifactWhere(id=artifact_id))

    if not artifact or artifact.dataset_id != dataset_id:
        raise ArtifactNotFound()

    return artifact


@artifacts_router.get(
    path="/{artifact_id}/preview",
    dependencies=[
        Depends(get_current_user),
    ]
)
async def preview_artifact(
    dataset_id: UUID,
    artifact_id: UUID,
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    uow: UnitOfWork = Depends(get_uow)
):
    artifact = await uow.artifacts.get_unique(ArtifactWhere(id=artifact_id))

    if not artifact or artifact.dataset_id != dataset_id:
        raise ArtifactNotFound()

    def _read_csv(filepath: str) -> dict[str, Any]:
        total_rows = sum(1 for _ in open(filepath)) - 1
        if total_rows < 0:
            total_rows = 0

        df = pd.read_csv(
            filepath,
            skiprows=range(1, offset + 1) if offset > 0 else None,
            nrows=limit
        )

        # Replace NaNs with None to avoid JSON serialization issues
        df = df.replace({float("nan"): None})

        return {
            "columns": df.columns.tolist(),
            "data": df.to_dict(orient="records"),
            "total": total_rows
        }

    with tempfile.NamedTemporaryFile(delete=True, suffix=".csv") as tmp:
        await uow.file_storage.download(path=artifact.path, destination=tmp.name)
        result = await run_in_threadpool(_read_csv, tmp.name)

    return result
