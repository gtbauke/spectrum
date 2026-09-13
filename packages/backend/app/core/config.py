import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_PATH = Path(__file__).resolve().parents[4]
ENV_FILE = Path(os.environ.get("ENV_FILE", ROOT_PATH / ".env"))
if not ENV_FILE.exists():
    candidate = Path.cwd() / ".env"
    if candidate.exists():
        ENV_FILE = candidate


class Settings(BaseSettings):
    ENV: str = "dev"

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "spectrum"

    DATABASE_URL: str = ""
    DATABASE_URL_SYNC: str = ""

    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_URL: str = ""

    FILE_STORAGE_SPECTRUM_DATA_PATH: str = ""
    STORAGE_TYPE: str = "local"
    STORAGE_BASE_URL: str | None = None

    S3_BUCKET: str = ""
    S3_REGION: str = "us-east-1"
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_ENDPOINT_URL: str | None = None

    SECRET_KEY: str = ""

    ADMIN_API_KEY: str = ""

    WORKER_HEARTBEAT_INTERVAL_SECONDS: int = 10
    WORKER_STALENESS_SECONDS: int = 30
    WORKER_TASK_TIMEOUT_SECONDS: int = 1200  # 20 minutes

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE) if ENV_FILE.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
