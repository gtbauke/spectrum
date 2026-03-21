from uuid import UUID

from core.utils.filters.field_filter import (
    DateTimeFilter, EnumFilter, NumberFilter, StringFilter, UUIDFilter)
from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter


class ModelWhere(BaseUniqueWhere):
    id: UUID


class ModelFilter(BaseFilter):
    id: UUIDFilter | None = None
    created_at: DateTimeFilter | None = None
    updated_at: DateTimeFilter | None = None
    profile_id: UUIDFilter | None = None
    name: StringFilter | None = None
    generated_by: UUIDFilter | None = None
    path: StringFilter | None = None
