from uuid import UUID
from pydantic import BaseModel

from core.features.profiles.profile import Profile
from core.features.profiles.profile_mode import ProfileMode


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
