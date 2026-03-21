from typing import Optional

from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter
from core.utils.filters.field_filter import BooleanFilter, DateTimeFilter


class AuthWhere(BaseUniqueWhere):
    token_hash: str


class AuthFilter(BaseFilter):
    revoked: Optional[BooleanFilter] = None
    expires_at: Optional[DateTimeFilter] = None
