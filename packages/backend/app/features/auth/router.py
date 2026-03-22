from uuid import UUID
from fastapi import APIRouter, Depends, Response, Request

from app.api.unit_of_work import get_uow
from db.adapters.unit_of_work import SqlAlchemyUnitOfWork

from app.services.encryption import EncryptionService
from app.services.jwt_service import JwtService
from app.features.auth.dtos.auth_credentials import AuthCredentials
from app.features.auth.guards.get_current_user import get_current_user
from app.features.users.errors.user_not_found import UserNotFound

from core.ports.unit_of_work import UnitOfWork
from core.features.users.where import UserWhere
from core.features.users.user import User

from .errors.invalid_credentials import InvalidCredentials
from .errors.invalid_token import InvalidTokenException
from .errors.forbidden import Forbidden

auth_router = APIRouter()


@auth_router.post("/login", description="Authenticate and receive access and refresh tokens via HttpOnly cookies")
async def login(
    credentials: AuthCredentials,
    response: Response,
    uow: UnitOfWork = Depends(get_uow),
    encryption_service: EncryptionService = Depends(EncryptionService),
    jwt_service: JwtService = Depends(JwtService)
):
    where = UserWhere(email=credentials.email)
    user = await uow.users.get_unique(where)

    if not user:
        raise InvalidCredentials()

    if not encryption_service.verify_password(credentials.password, user.password_hash):
        raise InvalidCredentials()

    access_token = jwt_service.create_access_token(user.id)
    refresh_token = jwt_service.create_refresh_token(user.id)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        secure=False
    )

    return {"message": "Login successful"}


@auth_router.get("/me", response_model=User, description="Get current authenticated user")
async def get_me(
    user_id: UUID = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    where = UserWhere(id=user_id)
    user = await uow.users.get_unique(where)

    if not user:
        raise UserNotFound()

    return user


@auth_router.post("/refresh", description="Refresh the access token using the refresh token cookie")
async def refresh_token(
    request: Request,
    response: Response,
    jwt_service: JwtService = Depends(JwtService)
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise InvalidTokenException()

    try:
        payload = jwt_service.decode_token(refresh_token)
        token_type = payload.get("type")
        if token_type != "refresh":
            raise InvalidTokenException()

        user_id = payload.get("sub")
        if not user_id:
            raise InvalidTokenException()
    except ValueError as e:
        raise Forbidden()

    new_access_token = jwt_service.create_access_token(user_id)
    new_refresh_token = jwt_service.create_refresh_token(user_id)

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        samesite="lax",
        secure=False
    )

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        samesite="lax",
        secure=False
    )

    return {"message": "Token refreshed"}


@auth_router.post("/logout", description="Logout the user by clearing the access and refresh token cookies")
async def logout(response: Response):
    response.delete_cookie("access_token", httponly=True,
                           samesite="lax", secure=False)
    response.delete_cookie("refresh_token", httponly=True,
                           samesite="lax", secure=False)

    return {"message": "Logged out successfully"}
