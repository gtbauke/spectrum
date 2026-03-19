from typing import Optional
from uuid import UUID

from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter
from core.utils.filters.field_filter import (
    UUIDFilter,
    DateTimeFilter,
    EnumFilter,
)


class JobRunWhere(BaseUniqueWhere):
    id: UUID


class JobRunFilter(BaseFilter):
    id: Optional[UUIDFilter] = None
    timestamp: Optional[DateTimeFilter] = None
    job_run_type: Optional[EnumFilter] = None
    job_id: Optional[UUIDFilter] = None
    started_at: Optional[DateTimeFilter] = None
    finished_at: Optional[DateTimeFilter] = None
