from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID
from jose import jwt, JWTError

from app.core.config import settings
from app.features.auth.errors.invalid_token import InvalidTokenException

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


class JwtService:
    def create_access_token(self, subject: str | UUID, expires_delta: timedelta | None = None) -> str:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + \
                timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self, subject: str | UUID, expires_delta: timedelta | None = None) -> str:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + \
                timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def decode_token(self, token: str) -> dict[str, Any]:
        """
        Decodes the token and returns the payload if valid.
        Raises ValueError if invalid or expired.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,
                                 algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise InvalidTokenException()
