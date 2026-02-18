import logging
from uuid import UUID

from app.api.deps import UnitOfWork
from core.models.datasets.dataset_status import DatasetStatus


logger = logging.getLogger(__name__)


class DatasetProcessingService:
    async def start_dataset_processing(
        self,
        *,
        uow: UnitOfWork,
        dataset_id: UUID,
    ) -> bool:
        dataset = await uow.datasets.get_for_update(dataset_id)

        if not dataset:
            return False

        logger.info("Starting processing for dataset with id %s", dataset_id, extra={
                    "dataset_id": dataset_id, "status": dataset.status})

        if dataset.status in (DatasetStatus.PROCESSING, DatasetStatus.COMPLETED):
            return False

        dataset.status = DatasetStatus.PROCESSING
        await uow.commit()

        return True

    async def fail_dataset_processing(
        self,
        *,
        uow: UnitOfWork,
        dataset_id: UUID,
        num_of_rows: int,
        num_of_features: int,
        error_message: str,
    ):
        dataset = await uow.datasets.get_for_update(dataset_id)

        if not dataset:
            return

        dataset.status = DatasetStatus.FAILED
        metadata = await uow.datasets_metadata.create_or_get_for_update(dataset_id)

        metadata.processing_attempts += 1
        metadata.last_processing_error = error_message
        metadata.num_rows = num_of_rows
        metadata.num_features = num_of_features

        await uow.commit()

    async def complete_dataset_processing(
        self,
        *,
        uow: UnitOfWork,
        dataset_id: UUID,
        num_of_rows: int,
        num_of_features: int,
    ):
        dataset = await uow.datasets.get_for_update(dataset_id)

        if not dataset:
            return

        dataset.status = DatasetStatus.COMPLETED
        metadata = await uow.datasets_metadata.create_or_get_for_update(dataset_id)

        metadata.num_rows = num_of_rows
        metadata.num_features = num_of_features
        metadata.last_processing_error = None

        await uow.commit()
