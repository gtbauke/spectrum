from __future__ import annotations

from uuid import UUID, uuid4
from pydantic import Field
from datetime import datetime, timezone

from core.models.base import BaseImmutableDomainModel

from .artifact_type import ArtifactType


class DatasetArtifact(BaseImmutableDomainModel):
    dataset_version_id: UUID = Field(
        ..., description="ID of the dataset version this artifact belongs to")

    artifact_type: ArtifactType = Field(
        ..., description="Type of the artifact, e.g., data, schema, stats, etc.")

    file_path: str = Field(...,
                           description="Path to the artifact file in storage")

    size_in_bytes: int = Field(...,
                               description="Size of the artifact file in bytes")
    checksum: str = Field(
        ..., description="Checksum of the artifact file for integrity verification")

    @classmethod
    def new(
        cls,
        *,
        dataset_version_id: UUID,
        artifact_type: ArtifactType,
        file_path: str,
        size_in_bytes: int,
        checksum: str,
    ) -> DatasetArtifact:
        return cls(
            id=uuid4(),
            dataset_version_id=dataset_version_id,
            artifact_type=artifact_type,
            file_path=file_path,
            size_in_bytes=size_in_bytes,
            checksum=checksum,
            timestamp=datetime.now(timezone.utc),
            version=1,
            is_latest=True,
        )
