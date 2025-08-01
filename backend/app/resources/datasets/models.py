from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Optional
from app.resources.jobs.models import Job


class CreateDataset(SQLModel):
    name: str
    description: Optional[str] = None
    dataset_file_path: Optional[str] = None


class Dataset(CreateDataset, table=True):
    __tablename__: str = "datasets"  # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    name: str = Field(max_length=255, unique=True)
    description: Optional[str] = Field(default=None)

    dataset_file_path: Optional[str] = Field(default=None,
                                             description="Path to the dataset file on the server")

    jobs: list[Job] = Relationship(back_populates="dataset")

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
