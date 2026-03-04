import secrets
import hashlib

from uuid import UUID

from jose import jwt
from datetime import datetime, timedelta

from .dtos.update_refresh_token import UpdateRefreshTokenDTO
from .dtos.create_refresh_token import CreateRefreshTokenDTO
from .where import AuthWhere

from app.core.config import settings

from core.repositories.auth import RefreshToken
from core.services.base import BaseService


class AuthService(BaseService[
    RefreshToken,
    AuthWhere,
    CreateRefreshTokenDTO,
    UpdateRefreshTokenDTO,
]):
    def create_access_token(self, user_id: UUID, expires_delta: timedelta):
        expire = datetime.now() + expires_delta
        to_encode: dict[str, str | datetime] = {
            "sub": str(user_id), "exp": expire}

        return jwt.encode(to_encode, settings.SECRET_KEY)

    def generate_refresh_token(self) -> str:
        random_string = secrets.token_urlsafe(64)
        return hashlib.sha256(random_string.encode()).hexdigest()
