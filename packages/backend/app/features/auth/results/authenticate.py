from pydantic import BaseModel, Field

from core.models.owners.owner import Owner
from core.models.users.user import User


class AuthenticateResult(BaseModel):
    user: User = Field(..., description="The authenticated user")
    owner: Owner = Field(...,
                         description="The owner associated with the authenticated user")
