from pydantic import BaseModel, Field
from datetime import timedelta

from core.models.users.user import User


class LoginResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    expires_in: timedelta = Field(...,
                                  description="Expiration delta time of the access token")

    user: User = Field(..., description="The authenticated user")


class RefreshResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    expires_in: timedelta = Field(...,
                                  description="Expiration delta time of the access token")
