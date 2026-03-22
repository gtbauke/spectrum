from pydantic import BaseModel, Field

class CreateProfileDto(BaseModel):
    name: str = Field(..., description="The name of the profile")
    description: str = Field(..., description="The description of the profile")
