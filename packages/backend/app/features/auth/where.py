from pydantic import Field
from core.utils.where import BaseWhere


class AuthWhere(BaseWhere):
    token_hash: str = Field(..., description="Hash of the refresh token")
