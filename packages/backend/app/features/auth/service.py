from fastapi import Response

from app.core.ports.unit_of_work import UnitOfWork
from app.features.auth.dtos.auth_credentials import AuthCredentials
from app.features.auth.errors.forbidden import Forbidden
from app.features.auth.errors.invalid_credentials import InvalidCredentials
from app.features.auth.errors.invalid_token import InvalidTokenException
from app.features.users.domain.user import User
from app.features.users.service import UsersService
from app.services.encryption import EncryptionService
from app.services.jwt_service import JwtService


class AuthService:
    def __init__(
        self,
        uow: UnitOfWork,
        users_service: UsersService,
        encryption_service: EncryptionService | None = None,
        jwt_service: JwtService | None = None,
    ) -> None:
        self._uow = uow
        self._users_service = users_service
        self._encryption = encryption_service or EncryptionService()
        self._jwt = jwt_service or JwtService()

    async def login(self, credentials: AuthCredentials, response: Response) -> User:
        user = await self._users_service.get_user_by_email(credentials.email)
        if not user:
            raise InvalidCredentials()

        if not self._encryption.verify_password(
            credentials.password, user.password_hash
        ):
            raise InvalidCredentials()

        access_token = self._jwt.create_access_token(user.id)
        refresh_token = self._jwt.create_refresh_token(user.id)

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="lax",
            secure=False,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="lax",
            secure=False,
        )

        return user

    async def refresh_tokens(self, refresh_token: str | None, response: Response) -> dict[str, str]:
        if not refresh_token:
            raise InvalidTokenException()

        try:
            payload = self._jwt.decode_token(refresh_token)
            token_type = payload.get("type")
            if token_type != "refresh":
                raise InvalidTokenException()

            user_id = payload.get("sub")
            if not user_id:
                raise InvalidTokenException()
        except ValueError:
            raise Forbidden()

        new_access_token = self._jwt.create_access_token(user_id)
        new_refresh_token = self._jwt.create_refresh_token(user_id)

        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            samesite="lax",
            secure=False,
        )
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            samesite="lax",
            secure=False,
        )

        return {"message": "Token refreshed"}

    def logout(self, response: Response) -> dict[str, str]:
        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")
        return {"message": "Logout successful"}
