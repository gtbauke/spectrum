from .base import BaseRepository

from core.models.users.user import User
from core.models.users.where import UsersWhere, UsersFilter


class BaseUsersRepository(BaseRepository[User, UsersWhere, UsersFilter]):
    pass
