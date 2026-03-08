from pydantic import BaseModel, Field
from uuid import UUID


class CreateDatasetVersionDTO(BaseModel):
    dataset_id: UUID = Field(...,
                             description="Unique identifier for the dataset")

    version: int = Field(
        default=1, ge=0, description="Version number of the dataset version")
