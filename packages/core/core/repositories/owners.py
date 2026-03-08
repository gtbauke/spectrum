from .base import BaseRepository

from core.models.owners.where import OwnersWhere, OwnersFilter
from core.models.owners.owner import Owner


class BaseOwnersRepository(BaseRepository[Owner, OwnersWhere, OwnersFilter]):
    pass
