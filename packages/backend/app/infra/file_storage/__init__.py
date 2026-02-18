from pathlib import Path

from app.infra.file_storage.local import LocalFileStorage
from app.core.config import settings

from core.common.file_storage.base import AbstractFileStorage


def get_file_storage() -> AbstractFileStorage:
    return LocalFileStorage(base_path=Path(settings.FILE_STORAGE_SPECTRUM_DATA_PATH))
