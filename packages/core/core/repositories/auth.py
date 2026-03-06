from .base import BaseRepository

from core.models.auth.where import AuthWhere
from core.models.auth.refresh_token import RefreshToken


class BaseAuthRepository(BaseRepository[RefreshToken, AuthWhere]):
    pass
