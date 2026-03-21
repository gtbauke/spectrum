from typing import Optional
from uuid import UUID

from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter
from core.utils.filters.field_filter import DateTimeFilter


class UserWhere(BaseUniqueWhere):
    id: Optional[UUID] = None
    email: Optional[str] = None


class UserFilter(BaseFilter):
    deleted_at: Optional[DateTimeFilter] = None
