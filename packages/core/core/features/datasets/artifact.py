from pydantic import Field
from uuid import UUID

from core.features.base import BaseImmutableDomainModel

from .artifact_role import ArtifactRole


class Artifact(BaseImmutableDomainModel):
    dataset_id: UUID = Field(..., description="The ID of the dataset")

    checksum: str = Field(..., description="The checksum of the dataset")

    size_in_bytes: int = Field(...,
                               description="The size of the dataset in bytes")

    path: str = Field(..., description="The path to the dataset")

    role: ArtifactRole = Field(..., description="The role of the dataset")
