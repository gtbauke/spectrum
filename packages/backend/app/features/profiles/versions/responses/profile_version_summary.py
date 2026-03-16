from __future__ import annotations
from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

from core.models.profiles.profile_version import ProfileVersion
from core.models.profiles.profile_visibility import ProfileVisibility


class ProfileVersionSummary(BaseModel):
    model_config = {
        "from_attributes": True,
    }

    id: UUID = Field(..., description="ID of the profile version entity")

    version: int = Field(
        ...,
        gt=0,
        description="Version of the profile"
    )

    timestamp: datetime = Field(...,
                                description="Date and time the profile version was created")

    is_latest: bool = Field(
        ..., description="Indicates if the profile version is the latest version associated with the profile")

    name: str = Field(
        ...,
        description="Name of the profile version"
    )

    description: Optional[str] = Field(None,
                                       description="Description of the profile version")

    visibility: ProfileVisibility = Field(
        ..., description="Indicates if the profile version is private or public")

    profile_id: UUID = Field(...,
                             description="ID of the profile this version belongs to")

    attached_dataset_count: int = Field(
        ..., description="Amount of datasets attached to the profile version")

    @classmethod
    def from_profile_version(cls, profile_version: ProfileVersion) -> ProfileVersionSummary:
        return cls(
            id=profile_version.id,
            version=profile_version.version,
            is_latest=profile_version.is_latest,
            name=profile_version.name,
            description=profile_version.description,
            timestamp=profile_version.timestamp,
            profile_id=profile_version.profile_id,
            visibility=profile_version.visibility,
            attached_dataset_count=len(profile_version.datasets),
        )
