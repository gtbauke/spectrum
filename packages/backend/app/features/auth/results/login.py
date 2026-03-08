from pydantic import BaseModel, Field


class LoginResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
