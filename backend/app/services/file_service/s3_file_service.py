from pathlib import Path
from typing import BinaryIO
from fastapi import Depends, logger
from sqlmodel import Session
from app.database import get_session
from app.services.file_service.file_service import FileService
from app.utils.config import Config
from botocore.exceptions import ClientError
from mypy_boto3_s3 import S3Client

import boto3


class S3FileService(FileService):
    """
    Service for handling uploads for AWS S3
    """

    def __init__(self) -> None:
        super().__init__()

        logger.logger.warning(f"AWS_ACCESS_KEY: {Config.AWS_ACCESS_KEY}")
        logger.logger.warning(f"AWS_SECRET_KEY: {Config.AWS_SECRET_KEY}")

        self.s3_instance: S3Client = boto3.client(  # type: ignore
            service_name="s3",
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_KEY,
            region_name=Config.S3_BUCKET_REGION
        )

    def on_server_start(self) -> None:
        return super().on_server_start()

    def on_server_shutdown(self, session: Session = Depends(get_session)) -> None:
        return super().on_server_shutdown(session)

    def upload_file(self, file: BinaryIO, destination: str) -> str:
        try:
            self.s3_instance.upload_fileobj(
                Fileobj=file, Bucket=Config.S3_BUCKET_NAME, Key=destination)
        except ClientError as e:
            logger.logger.error(e)
            raise e

        return f"https://{Config.S3_BUCKET_NAME}.s3.{Config.S3_BUCKET_REGION}.amazonaws.com/{destination}"

    def download_file(self, file_url: Path, destination: str) -> str:
        raise NotImplementedError

    def delete_file(self, file_path: Path) -> None:
        raise NotImplementedError

    def get_file_path(self, file_name: str) -> Path:
        raise NotImplementedError
