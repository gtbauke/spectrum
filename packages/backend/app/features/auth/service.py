import secrets
import hashlib

from uuid import UUID, uuid4

from jose import jwt
from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.features.auth.errors.invalid_token import InvalidTokenException
from app.features.auth.where import AuthWhere
from app.features.users.where import UsersWhere
from app.services.encryption import EncryptionService

from .dtos.auth_credentials import AuthCredentials
from .errors.invalid_credentials import InvalidCredentials

from core.ports.unit_of_work import UnitOfWork
from core.models.users.user import User
from core.models.auth.refresh_token import RefreshToken
from core.services.base import BaseService


class AuthService(BaseService):
    def __init__(self, encryption_service: EncryptionService):
        self._encryption_service = encryption_service

    def hash_token(self, token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    def create_access_token(self, user_id: UUID, expires_delta: timedelta):
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode: dict[str, str | datetime] = {
            "sub": str(user_id), "exp": expire}

        return jwt.encode(to_encode, settings.SECRET_KEY)

    async def revoke_refresh_token(self, *, uow: UnitOfWork, token_str: str) -> RefreshToken:
        token_hash = self.hash_token(token_str)
        token = await uow.auth.get_unique(where=AuthWhere(token_hash=token_hash))

        if not token or token.revoked:
            raise InvalidTokenException()

        await uow.auth.update(token.model_copy(
            update={"revoked": True}
        ))

        return token

    async def generate_refresh_token(self, *, uow: UnitOfWork, user_id: UUID) -> RefreshToken:
        random_string = secrets.token_urlsafe(64)
        token = self.hash_token(random_string)

        refresh_token = RefreshToken(
            id=uuid4(),
            user_id=user_id,
            token_hash=token,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7),
            revoked=False
        )

        await uow.auth.add(refresh_token)
        return refresh_token

    async def authenticate(self, *, uow: UnitOfWork, credentials: AuthCredentials) -> User:
        user = await uow.users.get_unique(where=UsersWhere(email=credentials.email))

        if not user:
            raise InvalidCredentials()

        if not self._encryption_service.verify_password(credentials.password, user.password_hash):
            raise InvalidCredentials()

        return user
