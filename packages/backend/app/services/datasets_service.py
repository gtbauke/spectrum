from uuid import UUID
from fastapi import UploadFile

from app.api.deps import UnitOfWork
from app.infra.file_storage.base import FileStorage
from app.infra.events.datasets.dataset_events_publisher import DatasetsEventsPublisher
from app.workers.schemas.dataset_processing_event import DatasetProcessingEvent
from app.db.models.dataset import Dataset, DatasetORM, DatasetStatus
from app.utils.checksum import calculate_upload_file_checksum


class DatasetsService:
    def __init__(
        self,
        storage: FileStorage,
        datasets_event_publisher: DatasetsEventsPublisher,
    ):
        self._storage = storage
        self._datasets_event_publisher = datasets_event_publisher

    async def create(self, uow: UnitOfWork, *, name: str, file: UploadFile) -> UUID:
        checksum = await calculate_upload_file_checksum(file)

        async with uow:
            dataset = Dataset.start_upload(name=name, checksum=checksum)

            orm = DatasetORM.from_domain(dataset)
            orm = await uow.datasets.add(orm)

            dataset_id = orm.id

        try:
            file_path = await self._storage.save(
                file=file,
                destination=f"datasets/{dataset.id}"
            )
        except Exception:
            async with uow:
                orm = await uow.datasets.get_by_id(dataset_id)

                if orm:
                    orm.status = DatasetStatus.FAILED
            raise

        async with uow:
            orm = await uow.datasets.get_by_id(dataset_id)

            if orm:
                orm.file_path = file_path

        event_payload = DatasetProcessingEvent(
            dataset_id=dataset_id,
            file_path=file_path,
        )

        await self._datasets_event_publisher.publish_dataset_processing_event(payload=event_payload)
        return dataset_id
