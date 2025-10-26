from typing import BinaryIO
from app.integrations.aws.s3_service import S3Service
from .storage_engine import StorageEngine
from app.logging_config import logger


class RemoteStorageEngine(StorageEngine):
    def __init__(self, remote_instance: S3Service):
        super().__init__()
        self.remote_instance = remote_instance

    async def get_file_path(self, key: str) -> str:
        return self.remote_instance.get_url(key)

    async def save_file_obj(self, file_obj: BinaryIO, key: str) -> str:
        logger.debug(f"{await self.get_file_path("test")}")

        self.remote_instance.upload_file_obj(key, file_obj)
        return await self.get_file_path(key)

    async def delete(self, key: str) -> None:
        self.remote_instance.delete(key)

    def get_presigned_url(self, key: str) -> str:
        return self.remote_instance.generate_presigned_url(key)

    def download_file(self, key: str, file_obj: BinaryIO):
        self.remote_instance.download(key, file_obj)
