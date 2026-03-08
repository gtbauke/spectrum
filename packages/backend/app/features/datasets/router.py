from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.features.auth.guards.get_current_user import get_current_owner
from app.api.unit_of_work import get_uow

from .service import DatasetsService, get_datasets_service
from .dto.create_dataset import CreateDatasetRouteDTO, CreateDatasetDTO
from .artifacts.router import dataset_artifacts_router

from core.ports.unit_of_work import UnitOfWork
from core.models.datasets.dataset import Dataset


datasets_router = APIRouter(tags=["datasets"])
datasets_router.include_router(
    prefix="/{dataset_id}/artifacts", router=dataset_artifacts_router)


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
