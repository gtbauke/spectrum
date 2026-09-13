from typing import Optional

from app.core.utils.where import BaseUniqueWhere
from app.core.utils.filters.base import BaseFilter
from app.core.utils.filters.field_filter import BooleanFilter, DateTimeFilter


class AuthWhere(BaseUniqueWhere):
    token_hash: str


class AuthFilter(BaseFilter):
    revoked: Optional[BooleanFilter] = None
    expires_at: Optional[DateTimeFilter] = None
