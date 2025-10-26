from typing import Callable, Optional
import boto3

from app.utils.config import Config
from app.logging_config import logger
from functools import lru_cache


class Boto3SessionOptions():
    def __init__(self, region_name: str, aws_access_key_id: str, aws_secret_access_key: str) -> None:
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key


def validate_property(options: list[str | Callable[[], str]]) -> str:
    value = ""
    for option in options:
        if callable(option):
            v = option()
            if v == "":
                continue
            else:
                value = v
                break
        else:
            if option == "":
                continue
            else:
                value = option
                break

    return value


def from_possible_none(obj: Optional[Boto3SessionOptions], func: Callable[[Boto3SessionOptions], str]):
    if obj is None:
        return ""

    return func(obj)


@lru_cache
def get_boto3_session(options: Optional[Boto3SessionOptions] = None):
    """
    Returns a singleton boto3 session using environment variables or IAM role.
    """

    region_name = validate_property([
        Config.S3_BUCKET_REGION,
        from_possible_none(options, lambda x: x.region_name)
    ])

    aws_access_key_id = validate_property([
        Config.AWS_ACCESS_KEY,
        from_possible_none(options, lambda x: x.aws_access_key_id)
    ])

    aws_secret_access_key = validate_property([
        Config.AWS_SECRET_KEY,
        from_possible_none(options, lambda x: x.aws_secret_access_key)
    ])

    logger.debug({
        "region_name": region_name,
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
    })

    return boto3.Session(
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
