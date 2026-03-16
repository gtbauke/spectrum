from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

from app.features.datasets.artifacts.responses.dataset_artifact_details import DatasetArtifactDetails
from core.models.datasets.artifact_type import ArtifactType
from core.models.datasets.dataset_artifact_version import DatasetArtifactVersion


class DatasetArtifactVersionDetails(BaseModel):
    id: UUID
    timestamp: datetime

    artifact_type: ArtifactType
    artifact: Optional[DatasetArtifactDetails]

    @classmethod
    def from_artifact_version(cls, av: DatasetArtifactVersion):
        return cls(
            id=av.id,
            timestamp=av.timestamp,
            artifact_type=av.artifact_type,
            artifact=DatasetArtifactDetails.from_artifact(
                av.dataset_artifact) if av.dataset_artifact is not None else None
        )
