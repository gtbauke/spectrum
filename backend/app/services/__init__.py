from app.services.file_service.file_service import FileService
from app.services.file_service.temporary_file_service import TemporaryFileService
from app.services.service import Service


def get_file_service() -> FileService:
    """
    Dependency to provide the FileService instance.
    This can be used in routes to access file operations.
    """
    return TemporaryFileService()


def get_all_services() -> list[Service]:
    return [get_file_service()]
