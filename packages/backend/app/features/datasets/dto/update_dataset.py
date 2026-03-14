from uuid import UUID
from pydantic import BaseModel, Field


class UpdateDatasetDTO(BaseModel):
    owner_id: UUID = Field(...,
                           description="The ID of the user who owns the dataset")
