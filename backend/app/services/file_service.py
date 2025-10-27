from io import BytesIO
from pathlib import Path
from typing import BinaryIO, Optional
from app.integrations.aws.s3_service import S3Service
from app.integrations.aws.session import Boto3SessionOptions
from app.services.engines.storage.local_storage_engine import LocalStorageEngine
from app.services.engines.storage.remote_storage_engine import RemoteStorageEngine
from app.services.engines.storage.storage_engine import StorageEngine
from app.services.engines.storage.temporary_storage_engine import TemporaryStorageEngine
from app.services.service import Service
from app.utils.config import Config
from app.logging_config import logger
from fastapi import Request
from enum import Enum


class FileServiceType(Enum):
    REMOTE = "REMOTE"
    LOCAL = "LOCAL"
    TEMP = "TEMP"


class FileService(Service):
    MAX_FILE_SIZE = 1024 * 1024

    def __init__(self, temp_engine_base_dir: str = "temp", options: Optional[Boto3SessionOptions] = None, file_service_type_override: Optional[FileServiceType] = None) -> None:
        super().__init__()

        self.local_engine = LocalStorageEngine()
        self.remote_engine = RemoteStorageEngine(
            S3Service(Config.S3_BUCKET_NAME, options))
        self.temp_engine = TemporaryStorageEngine(
            base_dir=temp_engine_base_dir, cleanup_interval=0)

        self.engine_mapping: dict[FileServiceType, StorageEngine] = {
            FileServiceType.REMOTE: self.remote_engine,
            FileServiceType.LOCAL: self.local_engine,
            FileServiceType.TEMP: self.temp_engine,
        }

        file_service_type = file_service_type_override if file_service_type_override is not None else FileServiceType(
            Config.FILE_SERVICE_TYPE)
        self.default_engine = self.engine_mapping[file_service_type]

    async def on_server_startup(self):
        await self.temp_engine.cleanup_expired_files()
        logger.info("Temporary files cleanup completed")

    async def on_server_shutdown(self):
        pass

    async def save_file_obj(self, file_obj: BinaryIO, key: str) -> Path | str:
        return await self.default_engine.save_file_obj(file_obj, key)

    async def download_from_remote(self, key: str):
        file_obj = BytesIO()
        self.remote_engine.download_file(key, file_obj)
        file_obj.seek(0)

        return file_obj


def get_file_service(request: Request) -> FileService:
    return request.app.state.file_service
