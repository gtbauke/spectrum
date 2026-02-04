from uuid import UUID
from aio_pika.abc import AbstractIncomingMessage

from app.workers.schemas.base import EventEnvelope
from app.workers.schemas.start_model_training_event import StartModelTrainingEvent
from app.services import get_datasets_service, get_model_training_service, get_models_service
from app.api.deps import get_uow


class DatasetNotFoundException(Exception):
    def __init__(self, dataset_id: UUID):
        self.dataset_id = dataset_id
        super().__init__(f"Dataset with ID {dataset_id} not found.")


class DatasetIsNotReadyException(Exception):
    def __init__(self, dataset_id: UUID):
        self.dataset_id = dataset_id
        super().__init__(
            f"Dataset with ID {dataset_id} is not ready for model training.")


async def handle_model_training_message(message: AbstractIncomingMessage) -> None:
    models_service = get_models_service()
    datasets_service = get_datasets_service()
    model_training_service = get_model_training_service()

    async with message.process():
        event_data = EventEnvelope[StartModelTrainingEvent].model_validate_json(
            message.body.decode()
        )

        async with get_uow() as uow:
            dataset = await datasets_service.get_by_id(uow=uow, dataset_id=event_data.payload.dataset_id)

            if not dataset:
                raise DatasetNotFoundException(event_data.payload.dataset_id)

            if not dataset.is_ready_for_model_training():
                raise DatasetIsNotReadyException(event_data.payload.dataset_id)

            await models_service.create(
                uow=uow,
                model_name=f"Model for dataset {dataset.name}",
                dataset_id=dataset.id,
                version=1,
            )

        if not dataset.file_path:
            raise DatasetNotFoundException(event_data.payload.dataset_id)

        await model_training_service.train_model(
            file_path=dataset.file_path
        )
