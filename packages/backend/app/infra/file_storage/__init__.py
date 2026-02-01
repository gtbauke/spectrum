from app.infra.file_storage.base import FileStorage
from app.infra.file_storage.local import LocalFileStorage


def get_file_storage() -> FileStorage:
    return LocalFileStorage(base_path="spectrum_data")
