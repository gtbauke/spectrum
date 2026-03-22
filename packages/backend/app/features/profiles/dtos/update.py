from pydantic import BaseModel, Field
from core.features.profiles.profile_mode import ProfileMode

class UpdateProfileDto(BaseModel):
    name: str | None = Field(None, description="The name of the profile")
    description: str | None = Field(None, description="The description of the profile")
    mode: ProfileMode | None = Field(None, description="The mode of the profile")
