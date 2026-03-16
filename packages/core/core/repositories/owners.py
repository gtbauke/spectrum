from .base import BaseRepository

from core.models.owners.where import OwnerWhere, OwnersFilter
from core.models.owners.owner import Owner


class BaseOwnersRepository(BaseRepository[Owner, OwnerWhere, OwnersFilter]):
    pass
