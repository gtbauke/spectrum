from typing import Optional
from uuid import UUID

from core.utils.filters.field_filter import StringFilter
from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter


class JobWhere(BaseUniqueWhere):
    id: Optional[UUID] = None
    profile_version_id: Optional[UUID] = None
    is_latest: Optional[bool] = None


class JobFilter(BaseFilter):
    name: Optional[StringFilter] = None
