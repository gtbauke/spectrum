import logging

from uuid import UUID
from jose import jwt, JWTError

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings


logger = logging.getLogger(__name__)
security = HTTPBearer()


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = jwt.decode(
            token.credentials, settings.SECRET_KEY, algorithms=["HS256"])
    except JWTError as e:
        logger.error(f"Error decoding JWT: {e}")
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials")

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials")

    return UUID(user_id)
