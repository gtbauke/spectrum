from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class CreateDatasetDTO(BaseModel):
    name: str = Field(..., description="The name of the dataset")

    description: Optional[str] = Field(
        None, description="A description of the dataset")

    owner_id: UUID = Field(...,
                           description="The ID of the user who owns the dataset")
