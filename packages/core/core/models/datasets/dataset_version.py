from __future__ import annotations

from uuid import UUID, uuid4
from pydantic import Field
from datetime import datetime, timezone

from core.models.base import BaseImmutableDomainModel

from .dataset_artifact_version import DatasetArtifactVersion


class DatasetVersion(BaseImmutableDomainModel):
    dataset_id: UUID = Field(...,
                             description="Unique identifier for the dataset")

    row_count: int = Field(..., description="Number of rows in the dataset")
    column_count: int = Field(...,
                              description="Number of columns in the dataset")

    artifacts: list[DatasetArtifactVersion] = Field(
        ...,
        description="List of artifacts associated with this dataset version"
    )

    @classmethod
    def new(cls, *, dataset_id: UUID, row_count: int, column_count: int, version: int) -> DatasetVersion:
        return cls(
            id=uuid4(),
            dataset_id=dataset_id,
            row_count=row_count,
            column_count=column_count,
            version=version,
            timestamp=datetime.now(timezone.utc),
            is_latest=True,
            artifacts=[],
        )
