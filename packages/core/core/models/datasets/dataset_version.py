from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from pydantic import Field
from datetime import datetime, timezone

from core.models.base import BaseImmutableVersionedDomainModel

from .dataset_artifact_version import DatasetArtifactVersion


class DatasetVersion(BaseImmutableVersionedDomainModel):
    name: str = Field(..., description="The name of the dataset")

    description: Optional[str] = Field(
        None, description="A brief description of the dataset")

    dataset_id: UUID = Field(...,
                             description="Unique identifier for the dataset")

    artifacts: list[DatasetArtifactVersion] = Field(
        ...,
        description="List of artifacts associated with this dataset version"
    )

    @classmethod
    def new(cls, *, dataset_id: UUID, version: int, name: str, description: Optional[str] = None) -> DatasetVersion:
        return cls(
            id=uuid4(),
            dataset_id=dataset_id,
            name=name,
            description=description,
            version=version,
            timestamp=datetime.now(timezone.utc),
            is_latest=True,
            artifacts=[],
        )
