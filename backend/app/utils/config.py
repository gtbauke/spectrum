from os import getenv


class Config:
    REDIS_URL: str = getenv("REDIS_URL", "redis://localhost:6379/0")
    DATABASE_URL: str = getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost/spectrum")

    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
