import logging
from aio_pika.abc import AbstractIncomingMessage

from app.workers.schemas.base import EventEnvelope
from app.workers.schemas.start_model_training_event import StartModelTrainingEvent
from app.services import (get_datasets_service, get_jobs_service,
                          get_model_training_service, get_models_service)
from app.api.deps import get_uow
from app.workers.consumers.datasets.errors.dataset_not_found_error import DatasetNotFoundError
from app.workers.consumers.models.errors.dataset_not_ready_for_training_error import DatasetNotReadyForTrainingError
from app.workers.consumers.models.errors.dataset_missing_file_path_error import DatasetMissingFilePathError
from app.domain.jobs.job_status import JobStatus

# TODO: handle exceptions, retry logic and job status updates in case of failure

logger = logging.getLogger(__name__)


async def handle_model_training_message(message: AbstractIncomingMessage) -> None:
    models_service = get_models_service()
    datasets_service = get_datasets_service()
    model_training_service = get_model_training_service()
    jobs_service = get_jobs_service()

    async with message.process():
        event_data = EventEnvelope[StartModelTrainingEvent].model_validate_json(
            message.body.decode()
        )

        async with get_uow() as uow:
            dataset = await datasets_service.get_by_id(uow=uow, dataset_id=event_data.payload.dataset_id)

            if not dataset:
                raise DatasetNotFoundError(event_data.payload.dataset_id)

            if not dataset.is_ready_for_model_training():
                raise DatasetNotReadyForTrainingError(
                    event_data.payload.dataset_id)

            job = await jobs_service.create(uow=uow, dataset=dataset)
            logger.info("Job created", extra={
                "job_id": job.id,
                "dataset_id": dataset.id,
            })

            model = await models_service.create(
                uow=uow,
                model_name=f"Model for dataset {dataset.name}",
                dataset_id=dataset.id,
                version=1,
            )

        if not dataset.file_path:
            raise DatasetMissingFilePathError(event_data.payload.dataset_id)

        await jobs_service.update_status(uow=uow, job_id=job.id, status=JobStatus.RUNNING)
        final_path = await model_training_service.train_model(
            dataset_id=dataset.id,
            dataset_file_name=dataset.file_path
        )

        async with get_uow() as uow:
            await models_service.update_model_file_path(
                uow=uow,
                model_id=model.id,
                model_file_path=final_path
            )

        await jobs_service.update_status(uow=uow, job_id=job.id, status=JobStatus.SUCCEEDED)
