import boto3

from app.utils.config import Config
from functools import lru_cache


@lru_cache
def get_boto3_session():
    """
    Returns a singleton boto3 session using environment variables or IAM role.
    """

    return boto3.Session(
        region_name=Config.S3_BUCKET_REGION,
        aws_access_key_id=Config.AWS_ACCESS_KEY,
        aws_secret_access_key=Config.AWS_SECRET_KEY,
    )
