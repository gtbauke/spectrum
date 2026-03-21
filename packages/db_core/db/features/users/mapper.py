from pydantic import SecretStr

from db.common.mappers.base import IMapper
from db.features.users.model import UserORM

from core.features.users.user import User


class UsersMapper(IMapper[UserORM, User]):
    @staticmethod
    def to_domain(orm: UserORM) -> User:
        return User(
            id=orm.id,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            deleted_at=orm.deleted_at,
            first_name=orm.first_name,
            last_name=orm.last_name,
            email=orm.email,
            password_hash=SecretStr(orm.password_hash),
        )

    @staticmethod
    def to_orm(domain: User) -> UserORM:
        return UserORM(
            id=domain.id,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            deleted_at=domain.deleted_at,
            first_name=domain.first_name,
            last_name=domain.last_name,
            email=domain.email,
            password_hash=domain.password_hash.get_secret_value(),
        )
