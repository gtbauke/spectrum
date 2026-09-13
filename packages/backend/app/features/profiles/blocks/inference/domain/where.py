from typing import Optional
from uuid import UUID
from app.core.utils.filters.field_filter import UUIDFilter
from app.core.utils.where import BaseUniqueWhere
from app.core.utils.filters.base import BaseFilter


class InferenceRunWhere(BaseUniqueWhere):
    id: UUID
    version: Optional[int] = None


class InferenceRunFilter(BaseFilter):
    block_id: Optional[UUIDFilter] = None
    profile_id: Optional[UUIDFilter] = None


class InferenceResultWhere(BaseUniqueWhere):
    id: Optional[UUID] = None


class InferenceResultFilter(BaseFilter):
    run_id: Optional[UUIDFilter] = None
