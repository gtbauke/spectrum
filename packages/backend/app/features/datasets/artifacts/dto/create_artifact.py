from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CreateArtifactDTO(BaseModel):
    dataset_id: UUID = Field(...,
                             description="ID of the dataset to which the artifact belongs")

    dataset_version_id: Optional[UUID] = Field(
        None, description="ID of the dataset version this artifacts belong to")
