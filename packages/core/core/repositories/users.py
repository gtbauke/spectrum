from .base import BaseRepository

from core.models.users.user import User
from core.models.users.where import UsersWhere


class BaseUsersRepository(BaseRepository[User, UsersWhere]):
    pass
