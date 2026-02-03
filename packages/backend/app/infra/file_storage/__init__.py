from app.infra.file_storage.base import FileStorage
from app.infra.file_storage.local import LocalFileStorage
from app.core.config import settings


def get_file_storage() -> FileStorage:
    return LocalFileStorage(base_path=settings.FILE_STORAGE_SPECTRUM_DATA_PATH)
