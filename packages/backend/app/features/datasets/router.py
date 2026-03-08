from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, status

from app.features.auth.guards.get_current_user import get_current_owner
from app.api.unit_of_work import get_uow

from .service import DatasetsService, get_datasets_service
from .results.create_dataset import CreateDatasetResult
from .dto.create_dataset import CreateDatasetRouteDTO, CreateDatasetDTO

from core.ports.unit_of_work import UnitOfWork


datasets_router = APIRouter(tags=["datasets"])


@datasets_router.post(
    path="/",
    response_model=CreateDatasetResult,
    status_code=status.HTTP_201_CREATED,
)
async def create_dataset(
    uow: UnitOfWork = Depends(get_uow),
    datasets_service: DatasetsService = Depends(get_datasets_service),
    current_owner: UUID = Depends(get_current_owner),
    route_data: CreateDatasetRouteDTO = Depends(CreateDatasetRouteDTO.as_form),
    file: UploadFile = File(...)
):
    data = CreateDatasetDTO(
        name=route_data.name,
        description=route_data.description,
        owner_id=current_owner
    )

    return await datasets_service.create(uow=uow, data=data, file=file.file)
