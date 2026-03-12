from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field

from core.models.profiles.profile_visibility import ProfileVisibility


class CreateProfileVersionWithProfileDTO(BaseModel):
    name: str = Field(..., max_length=255,
                      description="The name of the profile")

    description: Optional[str] = Field(
        None, description="A brief description of the profile")

    visibility: ProfileVisibility = Field(...,
                                          description="The visibility of the profile")


class CreateProfileDTO(BaseModel):
    owner_id: UUID
    version: Optional[CreateProfileVersionWithProfileDTO] = None


class CreateProfileRouteDTO(BaseModel):
    version: Optional[CreateProfileVersionWithProfileDTO] = None
