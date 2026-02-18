import logging

from datetime import datetime
from aio_pika.abc import AbstractIncomingMessage, AbstractChannel

from app.workers.schemas.base import EventEnvelope
from app.workers.schemas.start_model_training_event import StartModelTrainingEvent
from app.services import (DatasetsService, JobsService, ModelTrainingService, ModelsService, get_datasets_service, get_jobs_service,
                          get_model_training_service, get_models_service)
from app.api.deps import get_uow
from app.workers.consumers.datasets.errors.dataset_not_found_error import DatasetNotFoundError
from app.workers.consumers.models.errors.dataset_not_ready_for_training_error import DatasetNotReadyForTrainingError
from app.workers.consumers.models.errors.dataset_missing_file_path_error import DatasetMissingFilePathError
from core.models.jobs.job import Job
from core.models.jobs.job_status import JobStatus
from app.workers.utils.errors.retryable_error import RetryableError
from app.workers.utils.errors.unretryable_error import UnretryableError
from app.infra.events.rabbitmq import rabbitmq_manager
from app.infra.events.models.rabbit_mq_model_events_publisher import RabbitMQModelEventsPublisher
from app.workers.consumers.models.errors.model_not_found_error import ModelNotFoundError
from app.workers.consumers.models.errors.model_has_no_associated_job_error import ModelHasNoAssociatedJobError
from app.services.datasets.datasets_service import DatasetSearchBy

logger = logging.getLogger(__name__)


def _update_job_status_and_start_time(model: Job) -> Job:
    return model.model_copy(update={
        "status": JobStatus.RUNNING,
        "started_at": datetime.now(),
    })


def _update_job_status_and_end_time(model: Job) -> Job:
    return model.model_copy(update={
        "status": JobStatus.SUCCEEDED,
        "finished_at": datetime.now(),
    })


async def handle_start_model_training_event(
    event: StartModelTrainingEvent,
    models_service: ModelsService,
    datasets_service: DatasetsService,
    model_training_service: ModelTrainingService,
    jobs_service: JobsService,
):
    async with get_uow() as uow:
        dataset = await datasets_service.get_unique(
            uow=uow,
            where=DatasetSearchBy(dataset_id=event.dataset_id)
        )

        if not dataset:
            raise DatasetNotFoundError(event.dataset_id)

        if not dataset.is_ready_for_model_training():
            raise DatasetNotReadyForTrainingError(
                event.dataset_id)

        if event.model_id is None:
            job = await jobs_service.create(uow=uow, dataset=dataset)
            model = await models_service.create(
                uow=uow,
                model_name=f"Model for dataset {dataset.name}",
                dataset_id=dataset.id,
                job_id=job.id,
            )
        else:
            model = await models_service.get(uow=uow, model_id=event.model_id)

            if not model:
                raise ModelNotFoundError(event.model_id)

            if not model.job:
                raise ModelHasNoAssociatedJobError(event.model_id)

            job = model.job

    if not dataset.file_path:
        raise DatasetMissingFilePathError(event.dataset_id)

    await jobs_service.update(
        uow=get_uow(),
        job_id=job.id,
        update_func=_update_job_status_and_start_time
    )

    final_path = await model_training_service.train_model(
        uow=get_uow(),
        dataset_id=dataset.id,
        job_id=job.id,
        dataset_file_name=dataset.file_path
    )

    async with get_uow() as uow:
        await models_service.update_model_file_path(
            uow=uow,
            model_id=model.id,
            model_file_path=final_path
        )

        await models_service.record_model_job_run(
            uow=uow,
            model_id=model.id,
        )

    await jobs_service.update(
        uow=uow,
        job_id=job.id,
        update_func=_update_job_status_and_end_time
    )


async def handle_model_training_message(message: AbstractIncomingMessage, channel: AbstractChannel) -> None:
    models_service = get_models_service()
    datasets_service = get_datasets_service()
    model_training_service = get_model_training_service()
    jobs_service = get_jobs_service()

    model_events_publisher = RabbitMQModelEventsPublisher(
        connection=rabbitmq_manager.connection,
        channel=channel,
    )

    logger.info("Received message for model training",
                extra={"message_id": message.message_id})

    async with message.process():
        event_data = EventEnvelope[StartModelTrainingEvent].model_validate_json(
            message.body.decode()
        )

        logger.info(
            "Received StartModelTrainingEvent",
            extra={"dataset_id": event_data.payload.dataset_id},
        )

        try:
            await handle_start_model_training_event(
                event=event_data.payload,
                models_service=models_service,
                datasets_service=datasets_service,
                model_training_service=model_training_service,
                jobs_service=jobs_service,
            )
        except UnretryableError:
            await message.reject(requeue=False)
        except RetryableError:
            raw_retry_count = message.headers.get("x-retry-count", 0)

            if not isinstance(raw_retry_count, int):
                retry_count = 0
            else:
                retry_count = raw_retry_count

            if retry_count >= 5:
                await message.reject(requeue=False)
                return

            await model_events_publisher.publish_start_training_event(
                payload=event_data.payload,
                retry_count=retry_count + 1,
            )

            await message.ack()
