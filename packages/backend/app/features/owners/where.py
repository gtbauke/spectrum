from typing import Optional
from uuid import UUID

from core.utils.where import BaseWhere


class OwnersWhere(BaseWhere):
    id: Optional[UUID] = None
    user_id: Optional[UUID] = None
