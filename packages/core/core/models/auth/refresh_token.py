from uuid import UUID
from pydantic import Field
from datetime import datetime

from core.models.base import BaseDomainModel


class RefreshToken(BaseDomainModel):
    user_id: UUID = Field(...,
                          description="ID of the user associated with the refresh token")

    token_hash: str = Field(..., description="Hash of the refresh token")

    expires_at: datetime = Field(
        ..., description="Expiration time of the refresh token in ISO format")

    revoked: bool = Field(
        False, description="Indicates whether the refresh token has been revoked")
