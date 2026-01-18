import boto3

from mypy_boto3_s3 import S3Client
from boto3.s3.transfer import TransferConfig

from src.utils.env import ENV

s3: S3Client = boto3.client(  # type: ignore
    service_name="s3",
    region_name=ENV.AWS_REGION,
    aws_secret_access_key=ENV.AWS_SECRET_ACCESS_KEY,
    aws_access_key_id=ENV.AWS_ACCESS_KEY_ID
)

TRANSFER_CONFIG = TransferConfig(
    multipart_threshold=1024 * 1024 * 50,
    max_concurrency=5,
    use_threads=True
)


def upload_model(file_path: str, bucket: str, key: str) -> None:
    s3.upload_file(
        Filename=file_path,
        Bucket=bucket,
        Key=key,
        Config=TRANSFER_CONFIG
    )


def download_dataset(bucket: str, key: str, file_path: str) -> None:
    s3.download_file(
        Bucket=bucket,
        Key=key,
        Filename=file_path,
        Config=TRANSFER_CONFIG
    )
