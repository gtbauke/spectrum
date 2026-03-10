from typing import Optional
from uuid import UUID, uuid4
from pydantic import Field
from datetime import datetime, timezone

from core.models.base import BaseImmutableDomainModel

from .artifact_type import ArtifactType
from .dataset_artifact import DatasetArtifact


class DatasetArtifactVersion(BaseImmutableDomainModel):
    dataset_version_id: UUID = Field(
        ..., description="ID of the dataset version this artifact belongs to")

    dataset_artifact_id: UUID = Field(
        ..., description="ID of the dataset artifact this version belongs to")

    dataset_artifact: Optional[DatasetArtifact] = Field(
        None, description="The dataset artifact associated with this version")

    artifact_type: ArtifactType = Field(
        ..., description="Type of the artifact, e.g., data, schema, stats, etc.")

    @classmethod
    def new(
        cls,
        *,
        dataset_version_id: UUID,
        dataset_artifact_id: UUID,
        artifact_type: ArtifactType,
        dataset_artifact: Optional[DatasetArtifact] = None,
    ) -> "DatasetArtifactVersion":
        return cls(
            id=uuid4(),
            dataset_version_id=dataset_version_id,
            dataset_artifact_id=dataset_artifact_id,
            artifact_type=artifact_type,
            timestamp=datetime.now(timezone.utc),
            dataset_artifact=dataset_artifact,
        )
