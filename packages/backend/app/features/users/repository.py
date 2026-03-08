from core.repositories.users import BaseUsersRepository
from core.models.users.user import User
from core.models.users.where import UsersWhere, UsersFilter

from app.core.repository import BaseRepositoryImplementation

from .models import UserORM


class UsersRepository(BaseUsersRepository, BaseRepositoryImplementation[
    User,
    UserORM,
    UsersWhere,
    UsersFilter
]):
    orm_model = UserORM
