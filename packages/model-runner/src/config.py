from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    AWS_REGION: str = Field(default="sa-east-1")
    AWS_ACCESS_KEY_ID: str = Field(default="")
    AWS_SECRET_ACCESS_KEY: str = Field(default="")

    SQS_QUEUE_URL: str = Field(default="")
    ECS_CLUSTER: str = Field(default="")
    ECS_TASK_DEFINITION: str = Field(default="")
    CONTAINER_NAME: str = Field(default="")

    SUBNET_ID: str = Field(default="")
    DATABASE_URL: str = Field(default="")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


config = Config()
