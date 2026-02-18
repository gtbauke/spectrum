import logging

from typing import BinaryIO
from uuid import UUID

from core.ports.unit_of_work import UnitOfWork
from core.common.file_storage.transactional_file_storage import TransactionalFileStorage
from core.models.datasets.dataset_file import DatasetFile

logger = logging.getLogger(__name__)


class DatasetFilesService:
    async def save_dataset_file(
        self,
        *,
        uow: UnitOfWork,
        storage: TransactionalFileStorage,
        dataset_id: UUID,
        content: BinaryIO,
        original_file_name: str,
    ) -> str:
        uow.register(storage)

        raw_file = DatasetFile.new_raw_file(
            dataset_id=dataset_id,
            original_file_name=original_file_name,
        )

        await storage.stage(
            content=content,
            destination=raw_file.relative_path
        )

        return raw_file.file_name

    async def delete_dataset_file(
        self,
        *,
        uow: UnitOfWork,
        storage: TransactionalFileStorage,
        dataset_id: UUID,
        file_name: str,
    ) -> None:
        uow.register(storage)

        raw_file = DatasetFile.new_raw_file(
            dataset_id=dataset_id,
            original_file_name=file_name,
        )

        await storage.stage_delete(
            file_path=raw_file.relative_path
        )
