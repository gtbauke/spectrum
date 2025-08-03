from sqlmodel import Field, Relationship, SQLModel
from uuid import UUID, uuid4
from typing import Optional

from app.utils.sql_model_base import ModelBase
from app.resources.jobs.models import Job


class DatasetBase(ModelBase):
    name: str = Field(max_length=255, unique=True, index=True)
    description: Optional[str] = Field(default=None)
    dataset_file_path: Optional[str] = Field(
        default=None, description="Path to the dataset file on the server"
    )


class CreateDataset(DatasetBase):
    name: str
    description: Optional[str] = None
    dataset_file_path: Optional[str] = None


class Dataset(DatasetBase, table=True):
    __tablename__: str = "datasets"  # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    jobs: list[Job] = Relationship(back_populates="dataset")


class DatasetWithJobs(DatasetBase):
    id: UUID
    jobs: list[Job] = []


class DatasetFileUploadResponse(SQLModel):
    dataset: Dataset
    default_job: Job
