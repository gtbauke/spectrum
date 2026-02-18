import logging
import pandas as pd

from aio_pika.abc import AbstractIncomingMessage

from app.services import get_datasets_service
from app.services.datasets.datasets_service import DatasetSearchBy
from app.workers.schemas.dataset_processing_event import DatasetProcessingEvent
from app.workers.schemas.base import EventEnvelope
from app.api.deps import get_uow
from app.infra.events import get_model_events_publisher
from app.workers.schemas.start_model_training_event import StartModelTrainingEvent
from app.services.datasets.dataset_processing_service import DatasetProcessingService
from app.workers.consumers.datasets.errors.dataset_cannot_be_processed_error import DatasetCannotBeProcessedError
from app.workers.consumers.datasets.errors.missing_target_column_error import MissingTargetColumnError
from core.models.datasets.dataset_file import DatasetFile


logger = logging.getLogger(__name__)

# TODO: handle exceptions, retry logic and status updates in case of failure
# TODO: refactor all logic to standalone package


async def handle_dataset_processing_message(
    message: AbstractIncomingMessage
) -> None:
    dataset_processing_service = DatasetProcessingService()
    datasets_service = get_datasets_service()

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

            logger.info(
                "Received dataset processing event for dataset id %s. Can process: %s",
                event_data.payload.dataset_id,
                can_process,
                extra={
                    "dataset_id": event_data.payload.dataset_id,
                    "can_process": can_process,
                }
            )

            if not can_process:
                logger.warning(
                    "Dataset with id %s cannot be processed in its current state.",
                    event_data.payload.dataset_id,
                    extra={
                        "dataset_id": event_data.payload.dataset_id,
                    }
                )

                await dataset_processing_service.fail_dataset_processing(
                    uow=uow,
                    dataset_id=event_data.payload.dataset_id,
                    num_of_rows=0,
                    num_of_features=0,
                    error_message="Dataset cannot be processed in its current state.",
                )

                raise DatasetCannotBeProcessedError(
                    event_data.payload.dataset_id)

            dataset = await datasets_service.get_unique(
                uow=uow,
                where=DatasetSearchBy(dataset_id=event_data.payload.dataset_id)
            )

        if not dataset or not dataset.file_path:
            logger.warning(
                "Dataset with id %s not found or missing file path.",
                event_data.payload.dataset_id,
                extra={
                    "dataset_id": event_data.payload.dataset_id,
                }
            )

            async with get_uow() as uow:
                await dataset_processing_service.fail_dataset_processing(
                    uow=uow,
                    dataset_id=event_data.payload.dataset_id,
                    num_of_rows=0,
                    num_of_features=0,
                    error_message="Dataset not found or missing file path.",
                )

                raise DatasetCannotBeProcessedError(
                    event_data.payload.dataset_id)

        dataset_file = DatasetFile.new_raw_file(
            dataset_id=event_data.payload.dataset_id,
            original_file_name=dataset.file_path
        )

        logger.info(
            "Processing dataset with id %s located at %s",
            event_data.payload.dataset_id,
            dataset_file.relative_path,
            extra={
                "dataset_id": event_data.payload.dataset_id,
                "dataset_path": dataset_file.relative_path,
            }
        )

        data_frame = pd.read_csv(dataset_file.relative_path)  # type: ignore
        headers = data_frame.columns.tolist()

        has_target_column = "target" in headers
        num_of_features = len(headers) - (1 if has_target_column else 0)
        num_of_rows = len(data_frame)

        if not has_target_column:
            logger.warning(
                "Dataset with id %s is missing 'target' column.",
                event_data.payload.dataset_id,
                extra={
                    "dataset_id": event_data.payload.dataset_id,
                }
            )

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

        logger.info(
            "Completed processing dataset with id %s. Rows: %d, Features: %d",
            event_data.payload.dataset_id,
            num_of_rows,
            num_of_features,
            extra={
                "dataset_id": event_data.payload.dataset_id,
                "num_of_rows": num_of_rows,
                "num_of_features": num_of_features,
            }
        )

        await model_publisher.publish_start_training_event(
            StartModelTrainingEvent(
                dataset_id=event_data.payload.dataset_id,
            )
        )
