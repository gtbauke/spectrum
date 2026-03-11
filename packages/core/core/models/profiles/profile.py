from typing import Optional, TYPE_CHECKING
from uuid import UUID
from pydantic import Field

from core.models.base import BaseMutableDomainModel
from core.models.profiles.profile_status import ProfileStatus
from core.models.profiles.profile_visibility import ProfileVisibility


if TYPE_CHECKING:
    from core.models.profiles.profile_version import ProfileVersion


class Profile(BaseMutableDomainModel):
    name: str = Field(..., max_length=255,
                      description="The name of the profile")

    description: Optional[str] = Field(
        None, description="A brief description of the profile")

    status: ProfileStatus = Field(..., description="The status of the profile")

    visibility: ProfileVisibility = Field(...,
                                          description="The visibility of the profile")

    owner_id: UUID = Field(...,
                           description="The ID of the owner of the profile")

    versions: list["ProfileVersion"] = Field(...,
                                             description="The versions of the profile")
