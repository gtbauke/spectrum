import logging

from typing import Any
from uuid import UUID
from jose import jwt, JWTError

from fastapi import Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings
from .errors.invalid_jwt_token import InvalidJWTToken


logger = logging.getLogger(__name__)
security = HTTPBearer(auto_error=False)


def decode_jwt_token(token: str) -> dict[str, Any | None]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError as e:
        logger.error(f"Error decoding JWT: {e}")
        raise InvalidJWTToken()


def get_current_user(
    request: Request,
    token: HTTPAuthorizationCredentials | None = Depends(security)
):
    token_str = ""
    if token:
        token_str = token.credentials
    elif request.cookies.get("access_token"):
        token_str = request.cookies.get("access_token")

    if not token_str:
        raise InvalidJWTToken()

    payload = decode_jwt_token(token_str)

    user_id = payload.get("sub")
    if user_id is None:
        raise InvalidJWTToken()

    return UUID(user_id)
