from typing import Optional
from uuid import UUID

from core.utils.where import BaseUniqueWhere


class OwnersWhere(BaseUniqueWhere):
    id: Optional[UUID] = None
    user_id: Optional[UUID] = None
