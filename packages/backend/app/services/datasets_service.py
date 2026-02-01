from uuid import UUID
from fastapi import UploadFile

from app.api.deps import UnitOfWork
from app.infra.file_storage.base import FileStorage
from app.db.models.dataset import Dataset, DatasetORM, DatasetStatus


class DatasetsService:
    def __init__(
        self,
        storage: FileStorage,
    ):
        self._storage = storage

    async def create(self, uow: UnitOfWork, *, name: str, file: UploadFile) -> UUID:
        async with uow:
            dataset = Dataset.start_upload(name=name)

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
                orm = await uow.datasets.get(dataset_id)

                if orm:
                    orm.status = DatasetStatus.FAILED
            raise

        async with uow:
            orm = await uow.datasets.get(dataset_id)

            if orm:
                orm.status = DatasetStatus.PROCESSING
                orm.file_path = file_path

        return dataset_id
