from typing import Optional
from uuid import UUID

from core.utils.where import BaseUniqueWhere


class UsersWhere(BaseUniqueWhere):
    id: Optional[UUID] = None
    email: Optional[str] = None
