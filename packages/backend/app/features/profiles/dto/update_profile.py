from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field

from core.models.profiles.profile_visibility import ProfileVisibility


class UpdateProfileVersionWithProfileDTO(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    visibility: Optional[ProfileVisibility] = None


class UpdateProfileDTO(BaseModel):
    owner_id: UUID
    version: Optional[UpdateProfileVersionWithProfileDTO] = None


class UpdateProfileRouteDTO(BaseModel):
    version: Optional[UpdateProfileVersionWithProfileDTO] = None
