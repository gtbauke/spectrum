from uuid import UUID
from pydantic import BaseModel, Field


class LinkDatasetToProfile(BaseModel):
    dataset_ids: list[UUID] = Field(
        ..., description="The IDs of the datasets to link to the profile")
