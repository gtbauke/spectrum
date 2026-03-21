from pydantic import BaseModel, Field

from core.features.users.user import User


class AuthenticateResult(BaseModel):
    user: User = Field(..., description="The authenticated user")
