import pandas as pd

from aio_pika.abc import AbstractIncomingMessage

from app.workers.schemas.dataset_processing_event import DatasetProcessingEvent
from app.workers.schemas.base import EventEnvelope
from app.infra.file_storage import get_file_storage
from app.api.deps import get_uow
from app.db.models.dataset import DatasetMetadataORM
from app.domain.datasets.dataset_status import DatasetStatus
from app.domain.datasets.dataset_metadata import DatasetMetadata
from app.infra.events import get_model_events_publisher
from app.workers.schemas.start_model_training_event import StartModelTrainingEvent
from app.services.dataset_files_service import DatasetFilesService


async def handle_dataset_processing_message(
    message: AbstractIncomingMessage
) -> None:
    file_storage = get_file_storage()

    dataset_files_service = DatasetFilesService(file_storage=file_storage)
    model_publisher = get_model_events_publisher()

    async with message.process():
        event_data = EventEnvelope[DatasetProcessingEvent].model_validate_json(
            message.body.decode()
        )

        async with get_uow() as uow:
            dataset = await uow.datasets.get_for_update(event_data.payload.dataset_id)

            if not dataset:
                raise ValueError("Dataset not found")

            if dataset.status in (DatasetStatus.PROCESSING, DatasetStatus.COMPLETED):
                return

            dataset.status = DatasetStatus.PROCESSING
            await uow.commit()

        dataset_path = await dataset_files_service.get_dataset_file_path(file_name=event_data.payload.file_path)
        local_path = await file_storage.get_full_path(file_path=dataset_path)

        data_frame = pd.read_csv(local_path)  # type: ignore
        headers = data_frame.columns.tolist()

        has_target_column = "target" in headers
        num_of_features = len(headers) - (1 if has_target_column else 0)
        num_of_rows = len(data_frame)

        if not has_target_column:
            async with get_uow() as uow:
                dataset = await uow.datasets.get_for_update(event_data.payload.dataset_id)

                if not dataset:
                    raise ValueError("Dataset not found")

                dataset.status = DatasetStatus.FAILED

                metadata = DatasetMetadata(
                    dataset_id=dataset.id,
                    num_rows=num_of_rows,
                    num_features=num_of_features,
                    processing_attempts=1,
                    last_processing_error="Missing 'target' column in dataset.",
                )

                metadata_orm = DatasetMetadataORM.from_domain(metadata)

                await uow.datasets_metadata.add(metadata_orm)
                await uow.commit()

                raise ValueError("Missing 'target' column in dataset.")

        async with get_uow() as uow:
            dataset = await uow.datasets.get_for_update(event_data.payload.dataset_id)

            if not dataset:
                raise ValueError("Dataset not found")

            metadata = DatasetMetadata(
                dataset_id=dataset.id,
                num_rows=num_of_rows,
                num_features=num_of_features,
                processing_attempts=1,
                last_processing_error=None,
            )

            metadata_orm = DatasetMetadataORM.from_domain(metadata)
            dataset.status = DatasetStatus.COMPLETED

            await uow.datasets_metadata.add(metadata_orm)
            await uow.commit()

        await model_publisher.publish_start_training_event(
            StartModelTrainingEvent(
                dataset_id=event_data.payload.dataset_id,
            )
        )
