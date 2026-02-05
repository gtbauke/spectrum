import logging
import pandas as pd

from aio_pika.abc import AbstractIncomingMessage

from app.workers.schemas.dataset_processing_event import DatasetProcessingEvent
from app.workers.schemas.base import EventEnvelope
from app.infra.file_storage import get_file_storage
from app.api.deps import get_uow
from app.infra.events import get_model_events_publisher
from app.workers.schemas.start_model_training_event import StartModelTrainingEvent
from app.services.datasets.dataset_files_service import DatasetFilesService
from app.services.datasets.dataset_processing_service import DatasetProcessingService
from app.workers.consumers.datasets.errors.dataset_cannot_be_processed_error import DatasetCannotBeProcessedError
from app.workers.consumers.datasets.errors.missing_target_column_error import MissingTargetColumnError


logger = logging.getLogger(__name__)


async def handle_dataset_processing_message(
    message: AbstractIncomingMessage
) -> None:
    file_storage = get_file_storage()

    dataset_files_service = DatasetFilesService(file_storage=file_storage)
    dataset_processing_service = DatasetProcessingService()

    model_publisher = get_model_events_publisher()

    async with message.process():
        event_data = EventEnvelope[DatasetProcessingEvent].model_validate_json(
            message.body.decode()
        )

        async with get_uow() as uow:
            can_process = await dataset_processing_service.start_dataset_processing(
                uow=uow,
                dataset_id=event_data.payload.dataset_id,
            )

            if not can_process:
                await dataset_processing_service.fail_dataset_processing(
                    uow=uow,
                    dataset_id=event_data.payload.dataset_id,
                    num_of_rows=0,
                    num_of_features=0,
                    error_message="Dataset cannot be processed in its current state.",
                )

                raise DatasetCannotBeProcessedError(
                    event_data.payload.dataset_id)

        dataset_path = await dataset_files_service.get_dataset_file_path(
            file_name=event_data.payload.file_path,
            dataset_id=event_data.payload.dataset_id
        )

        logger.info(
            "Processing dataset with id %s located at %s",
            event_data.payload.dataset_id,
            dataset_path,
            extra={
                "dataset_id": event_data.payload.dataset_id,
                "dataset_path": dataset_path,
            }
        )

        data_frame = pd.read_csv(dataset_path)  # type: ignore
        headers = data_frame.columns.tolist()

        has_target_column = "target" in headers
        num_of_features = len(headers) - (1 if has_target_column else 0)
        num_of_rows = len(data_frame)

        if not has_target_column:
            async with get_uow() as uow:
                await dataset_processing_service.fail_dataset_processing(
                    uow=uow,
                    dataset_id=event_data.payload.dataset_id,
                    num_of_rows=num_of_rows,
                    num_of_features=num_of_features,
                    error_message="Missing 'target' column in dataset.",
                )

                raise MissingTargetColumnError(event_data.payload.dataset_id)

        async with get_uow() as uow:
            await dataset_processing_service.complete_dataset_processing(
                uow=uow,
                dataset_id=event_data.payload.dataset_id,
                num_of_rows=num_of_rows,
                num_of_features=num_of_features,
            )

        await model_publisher.publish_start_training_event(
            StartModelTrainingEvent(
                dataset_id=event_data.payload.dataset_id,
            )
        )
