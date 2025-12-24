import boto3

from config import Config

ecs = boto3.client(  # type: ignore
    service_name="ecs",
    region_name=Config.AWS_REGION,
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
)
