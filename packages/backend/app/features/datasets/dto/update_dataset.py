from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class UpdateDatasetDTO(BaseModel):
    name: Optional[str] = Field(None, description="The name of the dataset")

    description: Optional[str] = Field(
        None, description="A description of the dataset")

    owner_id: Optional[UUID] = Field(
        None, description="The UUID of the new owner")
