from __future__ import annotations

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

from app.features.profiles.associations.responses.profile_dataset_details import ProfileDatasetDetails
from app.features.profiles.blocks.responses.profile_block_details import ProfileBlockDetails

from core.models.profiles.profile_version import ProfileVersion
from core.models.profiles.profile_visibility import ProfileVisibility


class ProfileVersionDetails(BaseModel):
    id: UUID
    version: int
    is_latest: bool
    timestamp: datetime

    name: str
    description: Optional[str]
    visibility: ProfileVisibility

    datasets: list[ProfileDatasetDetails]
    blocks: list[ProfileBlockDetails]

    @classmethod
    def from_profile_version(cls, version: ProfileVersion) -> ProfileVersionDetails:
        return cls(
            id=version.id,
            version=version.version,
            is_latest=version.is_latest,
            timestamp=version.timestamp,
            name=version.name,
            description=version.description,
            visibility=version.visibility,
            datasets=[
                ProfileDatasetDetails.from_profile_dataset(pd)
                for pd in version.datasets
            ],
            blocks=[
                ProfileBlockDetails.from_profile_block(block)
                for block in version.blocks
            ],
        )
