from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID
from pydantic import Field

from core.models.base import BaseMutableDomainModel


if TYPE_CHECKING:
    from core.models.profiles.profile_version import ProfileVersion


class Profile(BaseMutableDomainModel):
    owner_id: UUID = Field(...,
                           description="The ID of the owner of the profile")

    versions: list["ProfileVersion"] = Field(...,
                                             description="The versions of the profile")

    @classmethod
    def new(cls, *, owner_id: UUID) -> "Profile":
        return cls(
            owner_id=owner_id,
            versions=[]
        )
