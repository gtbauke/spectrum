from __future__ import annotations

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

from app.features.owners.responses.owner_details import OwnerDetails
from app.features.profiles.versions.responses.profile_version_summary import ProfileVersionSummary
from app.features.users.responses.user_details import UserDetails

from core.models.profiles.profile import Profile


class ProfileSummary(BaseModel):
    model_config = {
        "from_attributes": True,
    }

    id: UUID = Field(..., description="ID of the profile")

    created_at: datetime = Field(...,
                                 description="Date and time when the profile was created")

    updated_at: datetime = Field(
        ..., description="Date and time when the profile was last updated")

    owner: OwnerDetails = Field(...,
                                description="Details about the profile owner entity")

    versions: list[ProfileVersionSummary] = Field(
        ..., description="Summary of the versions associated with this profile")

    @classmethod
    def from_profile(cls, profile: Profile) -> ProfileSummary:
        if not profile.owner.user:
            raise ValueError("Owners, for now, can only be users")

        return cls(
            id=profile.id,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
            versions=[
                ProfileVersionSummary.from_profile_version(profile_version)
                for profile_version in profile.versions
            ],
            owner=OwnerDetails(
                id=profile.owner_id,
                type=profile.owner.owner_type,
                details=UserDetails(
                    id=profile.owner.user.id,
                    email=profile.owner.user.email,
                    first_name=profile.owner.user.first_name,
                    last_name=profile.owner.user.last_name,
                    created_at=profile.owner.user.created_at,
                    updated_at=profile.owner.user.updated_at,
                    deleted_at=profile.owner.user.deleted_at,
                )
            )
        )
