import logging

from pathlib import Path
from typing import BinaryIO, Optional, cast

from core.ports.storage.file_storage import FileStorage
from core.ports.storage.path import SpectrumPath
from core.ports.storage.upload_result import UploadResult

logger = logging.getLogger(__name__)


class S3FileStorage(FileStorage):
    def __init__(
        self,
        bucket: str,
        region: str,
        access_key: str,
        secret_key: str,
        endpoint_url: Optional[str] = None,
    ) -> None:
        self._bucket = bucket
        self._region = region
        self._access_key = access_key
        self._secret_key = secret_key
        self._endpoint_url = endpoint_url

        # Verify aioboto3 availability
        try:
            import aioboto3
        except ImportError:
            logger.error(
                "aioboto3 is not installed. S3FileStorage will not function.")
            raise ImportError(
                "aioboto3 is required for S3FileStorage. Install it in the host package (backend/workers).")

    def _get_session(self):
        import aioboto3
        return aioboto3.Session(
            aws_access_key_id=self._access_key,
            aws_secret_access_key=self._secret_key,
            region_name=self._region,
        )

    async def upload(self, *, path: str, file: BinaryIO) -> UploadResult:
        from types_aiobotocore_s3.client import S3Client

        session = self._get_session()
        client: S3Client = cast(S3Client, session.client(
            "s3", endpoint_url=self._endpoint_url))

        async with client as s3:
            # Ensure we are at the beginning of the file
            file.seek(0)
            await s3.put_object(Bucket=self._bucket, Key=path, Body=file)

            # For S3, we use the key as the internal path
            spectrum_path = SpectrumPath(full_path=Path(path), path=Path(path))

            # Head the object to get size and potentially ETag for checksum
            response = await s3.head_object(Bucket=self._bucket, Key=path)
            size = response["ContentLength"]
            checksum = response.get("ETag", "").strip(
                '"')  # ETag is often the MD5

            return UploadResult(path=spectrum_path, size=size, checksum=checksum)

    async def download(self, *, path: str, destination: str) -> None:
        from types_aiobotocore_s3.client import S3Client

        destination_path = Path(destination).resolve()
        destination_path.parent.mkdir(parents=True, exist_ok=True)

        session = self._get_session()
        client: S3Client = cast(S3Client, session.client(
            "s3", endpoint_url=self._endpoint_url))

        async with client as s3:
            response = await s3.get_object(Bucket=self._bucket, Key=path)
            async with response["Body"] as stream:
                content = await stream.read()
                destination_path.write_bytes(content)

    async def generate_upload_url(
        self,
        *,
        path: str,
        expiration: int = 3600,
    ) -> str:
        from types_aiobotocore_s3.client import S3Client

        session = self._get_session()
        client = cast(S3Client, session.client(
            "s3", endpoint_url=self._endpoint_url))

        async with client as s3:
            url = await s3.generate_presigned_url(
                ClientMethod="put_object",
                Params={
                    "Bucket": self._bucket,
                    "Key": path,
                },
                ExpiresIn=expiration,
            )
            return url

    async def generate_download_url(
        self,
        *,
        path: str,
        expiration: int = 3600,
    ) -> str:
        from types_aiobotocore_s3.client import S3Client

        session = self._get_session()
        client = cast(S3Client, session.client(
            "s3", endpoint_url=self._endpoint_url))

        async with client as s3:
            url = await s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": self._bucket,
                    "Key": path,
                },
                ExpiresIn=expiration,
            )
            return url
