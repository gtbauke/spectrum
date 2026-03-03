from .base import BaseRepository
from core.models.users.user import User


class BaseUsersRepository(BaseRepository[User]):
    pass
