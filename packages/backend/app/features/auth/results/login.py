from pydantic import BaseModel, Field
from datetime import timedelta


class LoginResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    expires_in: timedelta = Field(...,
                                  description="Expiration delta time of the access token")
