from __future__ import annotations

from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from app.features.owners.responses.owner_details import OwnerDetails
from app.features.profiles.versions.responses.profile_version_details import ProfileVersionDetails
from app.features.users.responses.user_details import UserDetails
from core.models.profiles.profile import Profile


class ProfileDetails(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    owner: OwnerDetails
    latest_version: Optional[ProfileVersionDetails]

    @classmethod
    def from_profile(cls, profile: Profile) -> ProfileDetails:
        if not profile.owner.user:
            raise ValueError("Owners can only be users for now")

        return cls(
            id=profile.id,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
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
            ),
            latest_version=ProfileVersionDetails.from_profile_version(
                profile.versions[0]
            ) if profile.versions[0] else None,
        )
