from uuid import UUID
from fastapi import APIRouter, Depends

from app.api.v1.schemas.model import GetAllModelsResponse
from app.domain.models.model import Model
from app.db.uow.unit_of_work import UnitOfWork
from app.api.deps import get_uow
from app.services.models.models_service import ModelsService

models_router = APIRouter(tags=["models"])


@models_router.get(
    path="/non-trained",
    response_model=GetAllModelsResponse,
    status_code=200,
)
async def get_all_non_trained_models(
    uow: UnitOfWork = Depends(get_uow),
):
    service = ModelsService()

    async with uow:
        non_trained_models = await service.get_non_trained_models(uow=uow)

    return GetAllModelsResponse(models=non_trained_models)


@models_router.get(
    path="/trained",
    response_model=GetAllModelsResponse,
    status_code=200,
)
async def get_all_trained_models(
    uow: UnitOfWork = Depends(get_uow),
):
    service = ModelsService()

    async with uow:
        trained_models = await service.get_trained_models(uow=uow)

    return GetAllModelsResponse(models=trained_models)


@models_router.get(
    path="/{model_id}",
    response_model=Model,
    status_code=200,
)
async def get_model_by_id(
    model_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
):
    service = ModelsService()

    async with uow:
        model = await service.get(model_id=model_id, uow=uow)

    return model
