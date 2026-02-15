from uuid import UUID
from fastapi import APIRouter, Depends

from app.db.uow.unit_of_work import UnitOfWork
from app.api.deps import get_uow
from app.services.models.models_service import ModelsService
from app.domain.models.model import Model
from app.infra.events import ModelEventsPublisher, get_model_events_publisher
from app.infra.events.models.model_events_publisher import StartModelTrainingEvent
from app.services import get_model_training_service

models_router = APIRouter(tags=["models"])


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


@models_router.get(
    path="/",
    response_model=list[Model],
    status_code=200,
)
async def list_models(
    uow: UnitOfWork = Depends(get_uow),
):
    service = ModelsService()

    async with uow:
        models = await service.list(uow=uow)

    return models


@models_router.post(
    "/{model_id}/run",
    response_model=Model,
    status_code=200,
)
async def run_model(
    model_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
    model_events_publisher: ModelEventsPublisher = Depends(
        get_model_events_publisher)
):
    service = get_model_training_service()

    async with uow:
        model = await service.can_train_model(uow=uow, model_id=model_id)

        # TODO: handle errors
        if not model:
            raise ValueError(
                f"Model with ID {model_id} not found or is already running.")

        await model_events_publisher.publish_start_training_event(
            payload=StartModelTrainingEvent(
                dataset_id=model.dataset_id,
                model_id=model.id,
            )
        )

    return model
