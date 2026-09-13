from pydantic import BaseModel, Field

from app.features.profiles.domain.profile import Block
from app.features.profiles.domain.profile_mode import ProfileMode


class UpdateProfileDto(BaseModel):
    name: str | None = Field(None, description="The name of the profile")
    description: str | None = Field(
        None, description="The description of the profile")
    mode: ProfileMode | None = Field(
        None, description="The mode of the profile")

    blocks: list[Block] | None = Field(
        None, description="The blocks of the profile")
