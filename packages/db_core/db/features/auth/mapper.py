from core.features.auth.refresh_token import RefreshToken

from db.common.mappers.base import IMapper
from db.features.auth.model import RefreshTokenORM


class AuthMapper(IMapper[RefreshTokenORM, RefreshToken]):
    @staticmethod
    def to_domain(orm: RefreshTokenORM) -> RefreshToken:
        return RefreshToken(
            id=orm.id,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            expires_at=orm.expires_at,
            revoked=orm.revoked,
            token_hash=orm.token_hash,
            user_id=orm.user_id,
        )

    @staticmethod
    def to_orm(domain: RefreshToken) -> RefreshTokenORM:
        return RefreshTokenORM(
            id=domain.id,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            expires_at=domain.expires_at,
            revoked=domain.revoked,
            token_hash=domain.token_hash,
            user_id=domain.user_id,
        )
