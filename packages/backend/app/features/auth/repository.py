from app.core.repository import BaseRepositoryImplementation

from .models import RefreshTokenORM

from core.repositories.auth import BaseAuthRepository
from core.models.auth.refresh_token import RefreshToken
from core.models.auth.where import AuthFilter, AuthWhere


class AuthRepository(BaseAuthRepository, BaseRepositoryImplementation[
    RefreshToken, RefreshTokenORM, AuthWhere, AuthFilter
]):
    orm_model = RefreshTokenORM
