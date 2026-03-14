from typing import Optional

from pydantic import BaseModel, Field
from uuid import UUID


class CreateDatasetVersionDTO(BaseModel):
    name: str = Field(..., description="The name of the dataset")

    description: Optional[str] = Field(
        None, description="A brief description of the dataset")

    dataset_id: UUID = Field(...,
                             description="Unique identifier for the dataset")

    version: int = Field(
        default=1, ge=0, description="Version number of the dataset version")
