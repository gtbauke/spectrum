from app.services.file_service.file_service import FileService
from app.services.file_service.s3_file_service import S3FileService
from app.services.file_service.temporary_file_service import TemporaryFileService
from app.services.service import Service
from app.utils.config import Config

import logging


def get_file_service() -> FileService:
    logging.info(f"FileService: {Config.FILE_SERVICE_TYPE}")

    """
    Dependency to provide the FileService instance.
    This can be used in routes to access file operations.
    """
    if Config.FILE_SERVICE_TYPE == "s3":
        return S3FileService()

    return TemporaryFileService()


def get_all_services() -> list[Service]:
    return [get_file_service()]
