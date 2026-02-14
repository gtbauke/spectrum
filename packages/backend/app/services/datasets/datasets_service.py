from uuid import UUID
from fastapi import UploadFile

from app.api.deps import UnitOfWork
from app.infra.events.datasets.dataset_events_publisher import DatasetsEventsPublisher
from app.workers.schemas.dataset_processing_event import DatasetProcessingEvent
from app.db.models.dataset import Dataset, DatasetORM, DatasetStatus
from app.utils.checksum import calculate_upload_file_checksum
from app.services.datasets.dataset_files_service import DatasetFilesService
from app.services.datasets.errors.dataset_not_found_error import DatasetNotFoundError


class DatasetsService:
    def __init__(
        self,
        datasets_file_service: DatasetFilesService,
        datasets_event_publisher: DatasetsEventsPublisher,
    ):
        self._datasets_file_service = datasets_file_service
        self._datasets_event_publisher = datasets_event_publisher

    async def get_by_id(self, uow: UnitOfWork, *, dataset_id: UUID) -> Dataset | None:
        async with uow:
            orm = await uow.datasets.get_by_id(dataset_id)

            if orm:
                return orm.to_domain()

            return None

    async def create(self, uow: UnitOfWork, *, name: str, file: UploadFile) -> Dataset:
        checksum = await calculate_upload_file_checksum(file)

        async with uow:
            dataset = Dataset.start_upload(name=name, checksum=checksum)

            orm = DatasetORM.from_domain(dataset)
            orm = await uow.datasets.add(orm)

            dataset_id = orm.id

        try:
            file_path = await self._datasets_file_service.save_dataset_file(
                file=file,
                dataset_id=dataset_id,
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

        async with uow:
            dataset_model = await uow.datasets.get_by_id(dataset_id)

            if not dataset_model:
                raise DatasetNotFoundError(dataset_id)

        event_payload = DatasetProcessingEvent(
            dataset_id=dataset_id,
            file_path=file_path,
        )

        await self._datasets_event_publisher.publish_dataset_processing_event(
            payload=event_payload,
        )

        return dataset_model.to_domain()

    async def update_status(
        self,
        uow: UnitOfWork,
        *,
        dataset_id: UUID,
        status: DatasetStatus
    ) -> None:
        async with uow:
            orm = await uow.datasets.get_by_id(dataset_id)

            if not orm:
                raise DatasetNotFoundError(dataset_id)

            orm.status = status

    async def get_all(self, uow: UnitOfWork) -> list[Dataset]:
        async with uow:
            orms = await uow.datasets.list_all()
            return [orm.to_domain() for orm in orms]

    async def delete(self, uow: UnitOfWork, *, dataset_id: UUID) -> None:
        async with uow:
            orm = await uow.datasets.get_by_id(dataset_id)

            if not orm:
                raise DatasetNotFoundError(dataset_id)

            await uow.datasets.delete(orm)
