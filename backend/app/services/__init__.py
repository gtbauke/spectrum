from app.services.file_service.file_service import FileService
from app.services.file_service.s3_file_service import S3FileService
from app.services.file_service.temporary_file_service import TemporaryFileService
from app.services.service import Service
from app.utils.config import Config

import logging


def get_file_service(override: str | None = None, options: dict[str, str] | None = None) -> FileService:
    logging.info(f"FileService: {Config.FILE_SERVICE_TYPE}")

    """
    Dependency to provide the FileService instance.
    This can be used in routes to access file operations.
    """
    if override == "s3" or Config.FILE_SERVICE_TYPE == "s3":
        return S3FileService(options)

    return TemporaryFileService()


def get_all_services() -> list[Service]:
    return [get_file_service()]
