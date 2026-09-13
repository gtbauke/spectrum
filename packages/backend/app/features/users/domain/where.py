from typing import Optional
from uuid import UUID

from app.core.utils.where import BaseUniqueWhere
from app.core.utils.filters.base import BaseFilter
from app.core.utils.filters.field_filter import DateTimeFilter


class UserWhere(BaseUniqueWhere):
    id: Optional[UUID] = None
    email: Optional[str] = None


class UserFilter(BaseFilter):
    deleted_at: Optional[DateTimeFilter] = None
