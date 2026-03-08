from __future__ import annotations

from uuid import UUID, uuid4
from pydantic import Field
from datetime import datetime, timezone

from core.models.base import BaseImmutableDomainModel

from .dataset_artifact_version import DatasetArtifactVersion


class DatasetVersion(BaseImmutableDomainModel):
    dataset_id: UUID = Field(...,
                             description="Unique identifier for the dataset")

    artifacts: list[DatasetArtifactVersion] = Field(
        ...,
        description="List of artifacts associated with this dataset version"
    )

    @classmethod
    def new(cls, *, dataset_id: UUID, version: int) -> DatasetVersion:
        return cls(
            id=uuid4(),
            dataset_id=dataset_id,
            version=version,
            timestamp=datetime.now(timezone.utc),
            is_latest=True,
            artifacts=[],
        )
