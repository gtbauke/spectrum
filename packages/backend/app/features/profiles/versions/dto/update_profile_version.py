from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

from core.models.profiles.profile_status import ProfileStatus
from core.models.profiles.profile_visibility import ProfileVisibility


class UpdateProfileVersionDTO(BaseModel):
    name: str = Field(..., max_length=255,
                      description="The name of the profile")

    description: Optional[str] = Field(
        None, description="A brief description of the profile")

    status: ProfileStatus = Field(...,
                                  description="The status of the profile")

    visibility: ProfileVisibility = Field(...,
                                          description="The visibility of the profile")

    profile_id: UUID = Field(...,
                             description="The ID of the profile this version belongs to")
