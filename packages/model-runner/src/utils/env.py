from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    RABBITMQ_HOST: str = Field(alias="RABBITMQ_HOST", default="")
    RABBITMQ_PORT: str = Field(alias="RABBITMQ_PORT", default="5672")
    RABBITMQ_USERNAME: str = Field(alias="RABBITMQ_USERNAME", default="")
    RABBITMQ_PASSWORD: str = Field(alias="RABBITMQ_PASSWORD", default="")
    TASKS_EXCHANGE: str = Field(alias="TASKS_EXCHANGE", default="")
    TASKS_RETRY_EXCHANGE: str = Field(alias="TASKS_RETRY_EXCHANGE", default="")
    TASKS_DEAD_LETTER_EXCHANGE: str = Field(
        alias="TASKS_DEAD_LETTER_EXCHANGE", default="")
    TASKS_STATUS_EXCHANGE: str = Field(
        alias="TASKS_STATUS_EXCHANGE", default="")
    TASKS_QUEUE: str = Field(alias="TASKS_QUEUE", default="")
    TASKS_RETRY_QUEUE: str = Field(alias="TASKS_RETRY_QUEUE", default="")
    TASKS_DEAD_LETTER_QUEUE: str = Field(
        alias="TASKS_DEAD_LETTER_QUEUE", default="")
    TASKS_STATUS_QUEUE: str = Field(alias="TASKS_STATUS_QUEUE", default="")
    AWS_REGION: str = Field(alias="AWS_REGION", default="")
    AWS_ACCESS_KEY_ID: str = Field(alias="AWS_ACCESS_KEY_ID", default="")
    AWS_SECRET_ACCESS_KEY: str = Field(
        alias="AWS_SECRET_ACCESS_KEY", default="")
    S3_BUCKET_NAME: str = Field(alias="S3_BUCKET_NAME", default="")
    DATABASE_URL: str = Field(alias="DATABASE_URL", default="")

    TASKS_EXCHANGE_ROUTING_KEY: str = Field(
        alias="TASKS_EXCHANGE_ROUTING_KEY", default="")
    TASKS_DEAD_LETTER_ROUTING_KEY: str = Field(
        alias="TASKS_DEAD_LETTER_ROUTING_KEY", default="")
    TASKS_RETRY_ROUTING_KEY: str = Field(
        alias="TASKS_RETRY_ROUTING_KEY", default="")


ENV = EnvSettings()
