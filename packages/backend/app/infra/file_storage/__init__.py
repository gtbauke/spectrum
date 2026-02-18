from pathlib import Path

from app.infra.file_storage.local import LocalFileStorage
from app.core.config import settings

from app.infra.file_storage.local_transactional_file_storage import LocalTransactionalFileStorage
from core.common.file_storage.base import AbstractFileStorage
from core.common.file_storage.transactional_file_storage import TransactionalFileStorage


def get_file_storage() -> AbstractFileStorage:
    return LocalFileStorage(base_path=Path(settings.FILE_STORAGE_SPECTRUM_DATA_PATH))


def get_transactional_file_storage() -> TransactionalFileStorage:
    return LocalTransactionalFileStorage(
        base_path=Path(settings.FILE_STORAGE_SPECTRUM_DATA_PATH)
    )
