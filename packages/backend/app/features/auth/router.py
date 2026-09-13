from uuid import UUID
from fastapi import APIRouter, Depends, Response, Request

from app.api.unit_of_work import get_uow
from app.core.ports.unit_of_work import UnitOfWork
from app.features.auth.dtos.auth_credentials import AuthCredentials
from app.features.auth.guards.get_current_user import get_current_user
from app.features.auth.service import AuthService
from app.features.users.domain.user import User
from app.features.users.service import UsersService
from app.services.encryption import EncryptionService
from app.services.jwt_service import JwtService

auth_router = APIRouter()


def get_auth_service(
    uow: UnitOfWork = Depends(get_uow),
    encryption_service: EncryptionService = Depends(EncryptionService),
    jwt_service: JwtService = Depends(JwtService),
) -> AuthService:
    users_service = UsersService(uow=uow, encryption_service=encryption_service)
    return AuthService(
        uow=uow,
        users_service=users_service,
        encryption_service=encryption_service,
        jwt_service=jwt_service,
    )


def get_users_service(
    uow: UnitOfWork = Depends(get_uow),
    encryption_service: EncryptionService = Depends(EncryptionService),
) -> UsersService:
    return UsersService(uow=uow, encryption_service=encryption_service)


@auth_router.post("/login", description="Authenticate and receive access and refresh tokens via HttpOnly cookies")
async def login(
    credentials: AuthCredentials,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    await auth_service.login(credentials, response)
    return {"message": "Login successful"}


@auth_router.get("/me", response_model=User, description="Get current authenticated user")
async def get_me(
    user_id: UUID = Depends(get_current_user),
    users_service: UsersService = Depends(get_users_service),
):
    return await users_service.get_user_by_id(user_id)


@auth_router.post("/refresh", description="Refresh the access token using the refresh token cookie")
async def refresh_token(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    refresh_token_cookie = request.cookies.get("refresh_token")
    return await auth_service.refresh_tokens(refresh_token_cookie, response)


@auth_router.post("/logout", description="Logout the user by clearing the access and refresh token cookies")
async def logout(
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.logout(response)
