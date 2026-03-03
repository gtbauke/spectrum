from typing import Optional
from uuid import UUID

from core.utils.where import BaseWhere


class UsersWhere(BaseWhere):
    id: Optional[UUID] = None
    email: Optional[str] = None
