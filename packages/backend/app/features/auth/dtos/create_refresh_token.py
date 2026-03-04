from uuid import UUID

from pydantic import BaseModel, Field


class CreateRefreshTokenDTO(BaseModel):
    user_id: UUID = Field(...,
                          description="ID of the user to create the refresh token for")
