from os import getenv


class Config:
    REDIS_URL: str = getenv("REDIS_URL", "redis://localhost:6379/0")
    DATABASE_URL: str = getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost/spectrum")

    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL

    AWS_ACCESS_KEY: str = getenv("AWS_ACCESS_KEY", "")
    AWS_SECRET_KEY: str = getenv("AWS_SECRET_KEY", "")

    AWS_LOG_ACCESS_KEY: str = getenv("AWS_LOG_ACCESS_KEY", "")
    AWS_LOG_SECRET_KEY: str = getenv("AWS_LOG_SECRET_KEY", "")

    S3_BUCKET_NAME: str = getenv(
        "S3_BUCKET_NAME", "2a25affe-878a-44cd-aa91-c8e6a9de36ba-spectrum")

    S3_BUCKET_REGION: str = getenv("REGION_NAME", "sa-east-1")

    FILE_SERVICE_TYPE: str = getenv("FILE_SERVICE_TYPE", "TEMP")
