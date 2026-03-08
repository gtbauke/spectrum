from uuid import UUID
from pydantic import Field

from core.models.base import BaseImmutableDomainModel

from .artifact_type import ArtifactType


class DatasetArtifactVersion(BaseImmutableDomainModel):
    dataset_version_id: UUID = Field(
        ..., description="ID of the dataset version this artifact belongs to")

    dataset_artifact_id: UUID = Field(
        ..., description="ID of the dataset artifact this version belongs to")

    artifact_type: ArtifactType = Field(
        ..., description="Type of the artifact, e.g., data, schema, stats, etc.")
