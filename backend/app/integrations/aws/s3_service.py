from pathlib import Path
from typing import BinaryIO, Optional
from mypy_boto3_s3 import S3Client
from app.integrations.aws.session import Boto3SessionOptions, get_boto3_session


class S3Service:
    def __init__(self, bucket_name: str, options: Optional[Boto3SessionOptions] = None):
        self.session = get_boto3_session(options)
        self.client: S3Client = self.session.client("s3")  # type: ignore
        self.bucket_name = bucket_name

    def upload_file_obj(self, key: str, file_obj: BinaryIO):
        self.client.upload_fileobj(file_obj, self.bucket_name, key)

    def upload_file(self, key: str, file_path: Path):
        self.client.upload_file(str(file_path), self.bucket_name, key)

    def get_url(self, key: str) -> str:
        region = str(self.session.region_name)  # type: ignore
        return f"https://{self.bucket_name}.s3.{region}.amazonaws.com/{key}"

    def delete(self, key: str) -> None:
        self.client.delete_object(Bucket=self.bucket_name, Key=key)

    def generate_presigned_url(self, key: str) -> str:
        return self.client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": key,
            },
            ExpiresIn=3600,
        )

    def download(self, key: str, file_obj: BinaryIO):
        self.client.download_fileobj(self.bucket_name, key, file_obj)
