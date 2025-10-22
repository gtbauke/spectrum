from typing import BinaryIO
from mypy_boto3_s3 import S3Client
from app.integrations.aws.session import get_boto3_session


class S3Service:
    def __init__(self, bucket_name: str):
        self.session = get_boto3_session()
        self.client: S3Client = self.session.client("s3")  # type: ignore
        self.bucket_name = bucket_name

    def upload_file_obj(self, key: str, file_obj: BinaryIO):
        self.client.upload_fileobj(file_obj, self.bucket_name, key)

    def get_url(self, key: str) -> str:
        region = str(self.session.region_name)  # type: ignore
        return f"https://{self.bucket_name}.s3.{region}.amazonaws.com/{key}"
