from typing import Protocol

from core.common.repositories.base.mutable import IMutableRepository

from .user import User
from .where import UserWhere, UserFilter


class IUsersRepository(IMutableRepository[User, UserWhere, UserFilter], Protocol):
    pass
