from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status, Query

from app.features.auth.guards.get_current_user import get_current_owner
from app.api.unit_of_work import get_uow
from app.api.response import PaginatedResponse

from core.models.datasets.artifact_type import ArtifactType
from core.utils.filters.field_filter import EnumFilter, StringFilter

from .service import DatasetsService, get_datasets_service
from .dto.create_dataset import CreateDatasetRouteDTO, CreateDatasetDTO
from .artifacts.router import dataset_artifacts_router
from .versions.router import dataset_versions_router
from .guards.is_dataset_owner import is_dataset_owner

from core.ports.unit_of_work import UnitOfWork
from core.models.datasets.dataset import Dataset
from core.models.datasets.where import DatasetArtifactVersionsFilter, DatasetArtifactsFilter, DatasetVersionsFilter, DatasetsFilter, DatasetsWhere, NumberFilter


datasets_router = APIRouter(tags=["datasets"])

datasets_router.include_router(
    prefix="/{dataset_id}/artifacts", router=dataset_artifacts_router)

datasets_router.include_router(
    prefix="/{dataset_id}/versions", router=dataset_versions_router)


@datasets_router.post(
    path="/",
    response_model=Dataset,
    status_code=status.HTTP_201_CREATED,
)
async def create_dataset(
    route_data: CreateDatasetRouteDTO,
    uow: UnitOfWork = Depends(get_uow),
    datasets_service: DatasetsService = Depends(get_datasets_service),
    current_owner: UUID = Depends(get_current_owner),
):
    data = CreateDatasetDTO(
        name=route_data.name,
        description=route_data.description,
        owner_id=current_owner
    )

    return await datasets_service.create(uow=uow, data=data)


@datasets_router.get(
    path="/{dataset_id}/",
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(is_dataset_owner),
    ]
)
async def get_dataset(
    dataset_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
    datasets_service: DatasetsService = Depends(get_datasets_service),
):
    return await datasets_service.get_unique(uow=uow, where=DatasetsWhere(id=dataset_id))


@datasets_router.get(
    path="/search",
    status_code=status.HTTP_200_OK,
)
async def search_datasets(
    uow: UnitOfWork = Depends(get_uow),
    datasets_service: DatasetsService = Depends(get_datasets_service),
    size: int = Query(20, ge=1, le=100),
    page: int = Query(1, ge=1),
    min_size: Optional[int] = Query(None),
    max_size: Optional[int] = Query(None),
    name: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    artifact_type: Optional[ArtifactType] = Query(None),
    checksum: Optional[str] = Query(None),
):
    size_in_bytes_filter = any([min_size is not None, max_size is not None])
    artifact_filter = any([size_in_bytes_filter, checksum])
    artifacts_filter = any([artifact_type, size_in_bytes_filter, checksum])

    filters = DatasetsFilter(
        name=StringFilter(ilike=f"%{name}%") if name else None,
        description=StringFilter(
            ilike=f"%{description}%") if description else None,
        versions=DatasetVersionsFilter(
            artifacts=DatasetArtifactVersionsFilter(
                artifact_type=EnumFilter[ArtifactType](
                    eq=artifact_type
                ) if artifact_type else None,
                dataset_artifact=DatasetArtifactsFilter(
                    size_in_bytes=NumberFilter[int](
                        gte=min_size,
                        lte=max_size,
                    ) if size_in_bytes_filter else None,
                    checksum=StringFilter(eq=checksum) if checksum else None,
                ) if artifact_filter else None,
            ) if artifacts_filter else None,
        ) if artifacts_filter else None,
    )

    offset = (page - 1) * size
    items, total = await datasets_service.get_paginated(
        uow=uow,
        filter=filters,
        limit=size,
        offset=offset,
    )

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )
