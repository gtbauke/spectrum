from typing import Optional
from uuid import UUID
from pydantic import Field

from core.models.base import BaseImmutableDomainModel


class Model(BaseImmutableDomainModel):
    name: str = Field(..., description="The name of the model")

    description: Optional[str] = Field(...,
                                       description="The description of the model")

    profile_version_id: UUID = Field(
        ..., description="The ID of the profile version that this model belongs to"
    )

    dataset_version_id: UUID = Field(
        ..., description="The ID of the dataset version that this model was trained on")

    dataset_artifact_id: UUID = Field(
        ..., description="The ID of the dataset artifact that this model was trained on")

    generated_by: UUID = Field(...,
                               description="The ID of the job that generated this model")

    owner: UUID = Field(..., description="The ID of the owner of this model")
