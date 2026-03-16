from os import name

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

from app.features.datasets.artifact_version.responses.dataset_artifact_version_details import DatasetArtifactVersionDetails
from core.models.datasets.dataset_version import DatasetVersion


class DatasetVersionDetails(BaseModel):
    id: UUID
    version: int
    is_latest: bool
    timestamp: datetime

    name: str
    description: Optional[str]

    artifacts: list[DatasetArtifactVersionDetails]

    @classmethod
    def from_version(cls, v: DatasetVersion):
        return cls(
            id=v.id,
            version=v.version,
            timestamp=v.timestamp,
            is_latest=v.is_latest,
            name=v.name,
            description=v.description,
            artifacts=[
                DatasetArtifactVersionDetails.from_artifact_version(av)
                for av in v.artifacts
            ]
        )
