from sqlmodel import SQLModel, Field  # type: ignore
from enum import Enum


class Dataset(SQLModel, table=True):
    id: str = Field(primary_key=True)
    title: str
    description: str
    file_url: str = Field(alias="fileUrl")
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")


class ModelStatus(str, Enum):
    PENDING = "PENDING"
    TRAINING = "TRAINING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    QUEUED = "QUEUED"


class Model(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    version: str
    description: str
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")

    status: ModelStatus

    dataset_id: str = Field(foreign_key="dataset.id")
