from uuid import UUID
from pydantic import Field

from core.features.base import BaseMutableDomainModel


class Model(BaseMutableDomainModel):
    name: str = Field(..., description="The name of the model")

    profile_id: UUID = Field(..., description="The ID of the profile")

    generated_by: UUID = Field(..., description="The ID of the job")

    path: str = Field(..., description="The path to the binary model (e-graph dump)")
