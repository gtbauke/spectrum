from pydantic_settings import BaseSettings
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[4]


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

    model_config = {
        "env_file": str(ROOT_PATH / ".env"),
        "env_file_encoding": "utf-8",
    }


settings = Settings()
