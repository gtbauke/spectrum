from datetime import datetime
from pydantic import BaseModel, Field


class UpdateRefreshTokenDTO(BaseModel):
    expires_at: datetime = Field(...,
                                 description="New expiration time for the refresh token")

    revoked: bool = Field(...,
                          description="Whether the refresh token is revoked or not")
