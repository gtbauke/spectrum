from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime

from app.domain.datasets.dataset_status import DatasetStatus


class CreateDatasetRequest(BaseModel):
    name: str = Field(..., description="The name of the dataset")


class CreateDatasetResponse(BaseModel):
    id: UUID = Field(...,
                     description="The unique identifier of the created dataset")
    name: str = Field(..., description="The name of the created dataset")
    status: DatasetStatus = Field(...,
                                  description="The status of the created dataset")
    file_path: str | None = Field(
        None, description="The file path of the dataset, if available"
    )
    checksum: str | None = Field(
        None, description="The checksum of the dataset, if available"
    )
    created_at: datetime = Field(...,
                                 description="The creation timestamp of the dataset")
    updated_at: datetime = Field(...,
                                 description="The last update timestamp of the dataset")
