from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from uuid import UUID
from pydantic import Field

from core.models.base import BaseMutableDomainModel
from core.models.owners.owner import Owner


if TYPE_CHECKING:
    from core.models.profiles.profile_version import ProfileVersion


class Profile(BaseMutableDomainModel):
    owner_id: UUID = Field(...,
                           description="The ID of the owner of the profile")

    versions: list["ProfileVersion"] = Field(...,
                                             description="The versions of the profile")

    owner: "Owner" = Field(...,
                           description="The owner associated with this profile")

    @classmethod
    def new(cls, *, versions: list["ProfileVersion"] = [], owner: "Owner") -> "Profile":
        return cls(
            owner_id=owner.id,
            versions=versions,
            owner=owner,
        )
