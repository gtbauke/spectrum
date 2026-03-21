from .base import BaseRepository

from core.models.owners.where import OwnerWhere, OwnerFilter
from core.models.owners.owner import Owner


class BaseOwnersRepository(BaseRepository[Owner, OwnerWhere, OwnerFilter]):
    pass
