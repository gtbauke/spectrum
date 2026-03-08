from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.features.auth.guards.get_current_user import get_current_owner
from app.api.unit_of_work import get_uow

from .service import DatasetsService, get_datasets_service
from .dto.create_dataset import CreateDatasetRouteDTO, CreateDatasetDTO
from .artifacts.router import dataset_artifacts_router
from .versions.router import dataset_versions_router
from .guards.is_dataset_owner import is_dataset_owner

from core.ports.unit_of_work import UnitOfWork
from core.models.datasets.dataset import Dataset
from core.models.datasets.where import DatasetsWhere


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
