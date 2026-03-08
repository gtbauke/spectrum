from typing import Optional
from uuid import UUID

from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter


class OwnersWhere(BaseUniqueWhere):
    id: Optional[UUID] = None
    user_id: Optional[UUID] = None


class OwnersFilter(BaseFilter):
    pass
