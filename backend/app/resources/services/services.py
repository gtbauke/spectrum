from app.resources.services.file_service import FileService
from app.resources.services.temporary_file_service import TemporaryFileService
from app.resources.services.service import Service


async def get_file_service() -> FileService:
    """
    Dependency to provide the FileService instance.
    This can be used in routes to access file operations.
    """
    return TemporaryFileService()


async def get_all_services() -> list[Service]:
    return [await get_file_service()]
