from app.core.repository import BaseRepositoryImplementation

from .models import OwnerORM

from core.repositories.owners import BaseOwnersRepository
from core.models.owners.owner import Owner
from core.models.owners.where import OwnersFilter, OwnersWhere


class OwnersRepository(BaseOwnersRepository, BaseRepositoryImplementation[
    Owner, OwnerORM, OwnersWhere, OwnersFilter
]):
    orm_model = OwnerORM
