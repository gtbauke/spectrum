from os import getenv


class Config:
    REDIS_URL = getenv("REDIS_URL", "redis://localhost:6379/0")
    POSTGRES_URL = getenv(
        "POSTGRES_URL", "postgresql://postgres:postgres@localhost/spectrum")

    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
