from datetime import datetime
from typing import Optional, Sequence

from app.db.models.outbox import AggregateType
from app.services.outbox.outbox_service import CreateOutboxData, OutboxService
from app.utils.checksum import calculate_upload_file_checksum

from app.db.models.dataset import Dataset

from app.services.datasets.dataset_files_service import DatasetFilesService
from app.services.datasets.errors.dataset_not_found_error import DatasetNotFoundError
from app.services.datasets.utils.dataset_search_by import DatasetSearchBy
from app.services.datasets.utils.create_dataset import CreateDatasetData
from app.services.datasets.utils.update_dataset import UpdateDatasetData

from core.common.file_storage.transactional_file_storage import TransactionalFileStorage
from core.ports.unit_of_work import UnitOfWork
from core.services.base import BaseService
from core.tasks.datasets.payload import DatasetProcessTaskPayload
from core.tasks.types import TaskType


class DatasetsService(BaseService[
    Dataset,
    DatasetSearchBy,
    CreateDatasetData,
    UpdateDatasetData
]):
    def __init__(
        self,
        datasets_file_service: DatasetFilesService,
        outbox_service: OutboxService[DatasetProcessTaskPayload],
        storage: TransactionalFileStorage,
    ):
        self._datasets_file_service = datasets_file_service
        self._outbox_service = outbox_service
        self._storage = storage

    async def get_unique(self, *, uow: UnitOfWork, where: DatasetSearchBy) -> Optional[Dataset]:
        async with uow:
            return await uow.datasets.get_by_id(id=where.dataset_id)

    async def create(self, *, uow: UnitOfWork, data: CreateDatasetData) -> Dataset:
        checksum = await calculate_upload_file_checksum(data.file)

        async with uow:
            dataset = Dataset.start_upload(name=data.name, checksum=checksum)
            file_name = await self._datasets_file_service.save_dataset_file(
                uow=uow,
                content=data.file.file,
                dataset_id=dataset.id,
                original_file_name=data.file.filename or "unknown",
                storage=self._storage,
            )

            dataset = dataset.attach_file(file_name=file_name)
            await uow.datasets.add(dataset)

            # TODO: create worker for publishing events
            await self._outbox_service.create(
                uow=uow,
                data=CreateOutboxData[DatasetProcessTaskPayload](
                    aggregate_type=AggregateType.DATASET,
                    aggregate_id=dataset.id,
                    event_type=TaskType.DATASET_PROCESSING,
                    event_version=1,
                    available_at=datetime.now(),
                    payload=DatasetProcessTaskPayload(
                        dataset_id=dataset.id,
                    )
                )
            )

        return dataset

    async def update_unique(self, *, uow: UnitOfWork, where: DatasetSearchBy, data: UpdateDatasetData) -> Dataset:
        async with uow:
            dataset = await uow.datasets.get_by_id(where.dataset_id)

            if not dataset:
                raise DatasetNotFoundError(where.dataset_id)

            dataset = dataset.model_copy(
                update=data.model_dump(exclude_unset=True)
            )

            await uow.datasets.update(dataset)
            return dataset

    async def delete_unique(self, *, uow: UnitOfWork, where: DatasetSearchBy) -> None:
        async with uow:
            await uow.datasets.delete(where.dataset_id)

    async def get_all(self, *, uow: UnitOfWork) -> Sequence[Dataset]:
        async with uow:
            return await uow.datasets.list_all()
