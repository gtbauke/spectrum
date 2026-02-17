from typing import Optional, Sequence

from app.api.deps import UnitOfWork
from app.utils.checksum import calculate_upload_file_checksum

from app.db.models.dataset import Dataset, DatasetORM, DatasetStatus
from app.infra.events.datasets.dataset_events_publisher import DatasetsEventsPublisher
from app.workers.schemas.dataset_processing_event import DatasetProcessingEvent

from app.services.base import BaseService
from app.services.datasets.dataset_files_service import DatasetFilesService
from app.services.datasets.errors.dataset_not_found_error import DatasetNotFoundError
from app.services.datasets.utils.dataset_search_by import DatasetSearchBy
from app.services.datasets.utils.create_dataset import CreateDatasetData
from app.services.datasets.utils.update_dataset import UpdateDatasetData


class DatasetsService(BaseService[
    Dataset,
    DatasetSearchBy,
    CreateDatasetData,
    UpdateDatasetData
]):
    def __init__(
        self,
        datasets_file_service: DatasetFilesService,
        datasets_event_publisher: DatasetsEventsPublisher,
    ):
        self._datasets_file_service = datasets_file_service
        self._datasets_event_publisher = datasets_event_publisher

    async def get_unique(self, *, uow: UnitOfWork, where: DatasetSearchBy) -> Optional[Dataset]:
        async with uow:
            orm = await uow.datasets.get_by_id(where.dataset_id)

            if not orm:
                return None

            return orm.to_domain()

    async def create(self, *, uow: UnitOfWork, data: CreateDatasetData) -> Dataset:
        checksum = await calculate_upload_file_checksum(data.file)

        async with uow:
            dataset = Dataset.start_upload(name=data.name, checksum=checksum)

            orm = DatasetORM.from_domain(dataset)
            orm = await uow.datasets.add(orm)

            dataset_id = orm.id

        try:
            file_path = await self._datasets_file_service.save_dataset_file(
                file=data.file,
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

    async def update_unique(self, *, uow: UnitOfWork, where: DatasetSearchBy, data: UpdateDatasetData) -> Dataset:
        async with uow:
            orm = await uow.datasets.get_for_update(where.dataset_id)

            if not orm:
                raise DatasetNotFoundError(where.dataset_id)

            update_data = data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(orm, field, value)

            await uow.flush()
            domain = orm.to_domain()

        return domain

    async def delete_unique(self, *, uow: UnitOfWork, where: DatasetSearchBy) -> None:
        async with uow:
            orm = await uow.datasets.get_by_id(where.dataset_id)

            if not orm:
                raise DatasetNotFoundError(where.dataset_id)

            await uow.datasets.delete(orm)
            await self._datasets_file_service.delete_dataset(dataset_id=where.dataset_id)

    async def get_all(self, *, uow: UnitOfWork) -> Sequence[Dataset]:
        async with uow:
            orms = await uow.datasets.list_all()
            return [orm.to_domain() for orm in orms]
