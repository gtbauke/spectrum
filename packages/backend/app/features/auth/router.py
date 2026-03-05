import logging

from datetime import timedelta
from uuid import UUID

from fastapi import APIRouter, Response, Depends, Cookie

from app.api.unit_of_work import get_uow
from app.features.auth.responses.login import LoginResponse
from app.features.users.service import UsersService, get_users_service
from app.features.users.where import UsersWhere
from app.services.encryption import EncryptionService

from core.ports.unit_of_work import UnitOfWork

from .guards.get_current_user import get_current_user
from .dtos.auth_credentials import AuthCredentials
from .service import AuthService

logger = logging.getLogger(__name__)

# TODO: handle errors and return appropriate status codes and messages
# right now, invalid credentials are breaking the app
auth_router = APIRouter(tags=["auth"])


def get_auth_service() -> AuthService:
    return AuthService(EncryptionService())


@auth_router.post("/login", response_model=LoginResponse)
async def login(
    response: Response,
    credentials: AuthCredentials,
    uow: UnitOfWork = Depends(get_uow),
    auth_service: AuthService = Depends(get_auth_service)
):
    user = await auth_service.authenticate(uow=uow, credentials=credentials)

    access_token = auth_service.create_access_token(
        user_id=user.id, expires_delta=timedelta(minutes=15))
    refresh_token = await auth_service.generate_refresh_token(uow=uow, user_id=user.id)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token.token_hash,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,  # 7 days in seconds
    )

    return LoginResponse(access_token=access_token)


@auth_router.get("/me")
async def get_me(
    user_id: UUID = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow),
    users_service: UsersService = Depends(get_users_service),
):
    return await users_service.get_unique(uow=uow, where=UsersWhere(id=user_id))


@auth_router.post("/refresh")
async def refresh(
    response: Response,
    refresh_token: str = Cookie(...),
    uow: UnitOfWork = Depends(get_uow),
    auth_service: AuthService = Depends(get_auth_service),
):
    logger.info("Refreshing access token for refresh token: %s", refresh_token)
    revoked_token = await auth_service.revoke_refresh_token(uow=uow, token_str=refresh_token)

    new_refresh_token = await auth_service.generate_refresh_token(uow=uow, user_id=revoked_token.user_id)
    access_token = auth_service.create_access_token(
        user_id=revoked_token.user_id, expires_delta=timedelta(minutes=15))

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token.token_hash,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,  # 7 days in seconds
    )

    return LoginResponse(access_token=access_token)


@auth_router.post("/logout")
async def logout(
    refresh_token: str = Cookie(...),
    uow: UnitOfWork = Depends(get_uow),
    auth_service: AuthService = Depends(get_auth_service),
):
    await auth_service.revoke_refresh_token(uow=uow, token_str=refresh_token)
