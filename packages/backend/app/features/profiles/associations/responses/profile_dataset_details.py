from __future__ import annotations

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

from app.features.datasets.versions.responses.dataset_version_details import DatasetVersionDetails
from core.models.profiles.profile_dataset_association import ProfileDatasetAssociation
from core.models.profiles.profile_dataset_role import ProfileDatasetRole


class ProfileDatasetDetails(BaseModel):
    id: UUID
    timestamp: datetime

    role: ProfileDatasetRole
    dataset_version: Optional[DatasetVersionDetails]

    @classmethod
    def from_profile_dataset(cls, ds: ProfileDatasetAssociation) -> ProfileDatasetDetails:
        return cls(
            id=ds.id,
            timestamp=ds.timestamp,
            role=ds.role,
            dataset_version=DatasetVersionDetails.from_version(
                ds.dataset_version) if ds.dataset_version is not None else None
        )
