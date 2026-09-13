from uuid import UUID
from pydantic import BaseModel

from app.features.profiles.domain.profile import Profile
from app.features.profiles.domain.profile_mode import ProfileMode


class ProfileSummary(BaseModel):
    id: UUID

    name: str
    mode: ProfileMode

    @classmethod
    def from_profile(cls, profile: Profile) -> "ProfileSummary":
        return cls(
            id=profile.id,
            name=profile.name,
            mode=profile.mode,
        )
