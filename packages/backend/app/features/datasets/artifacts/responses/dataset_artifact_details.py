from __future__ import annotations

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from core.models.datasets.dataset_artifact import DatasetArtifact


class DatasetArtifactDetails(BaseModel):
    id: UUID
    timestamp: datetime

    file_path: str
    size_in_bytes: int

    checksum: str

    @classmethod
    def from_artifact(cls, artifact: DatasetArtifact):
        return cls(
            id=artifact.id,
            timestamp=artifact.timestamp,
            file_path=artifact.file_path,
            size_in_bytes=artifact.size_in_bytes,
            checksum=artifact.checksum,
        )
