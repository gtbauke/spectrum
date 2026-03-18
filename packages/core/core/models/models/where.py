from typing import Optional
from uuid import UUID

from core.utils.filters.field_filter import DateTimeFilter, StringFilter, UUIDFilter
from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter


class ModelWhere(BaseUniqueWhere):
    id: Optional[UUID] = None
    name: Optional[str] = None
    profile_version_id: Optional[UUID] = None
    dataset_version_id: Optional[UUID] = None
    dataset_artifact_id: Optional[UUID] = None
    generated_by: Optional[UUID] = None
    owner: Optional[UUID] = None


class ModelFilter(BaseFilter):
    id: Optional[UUIDFilter] = None
    timestamp: Optional[DateTimeFilter] = None

    name: Optional[StringFilter] = None
    description: Optional[StringFilter] = None

    profile_version_id: Optional[UUIDFilter] = None
    dataset_version_id: Optional[UUIDFilter] = None
    dataset_artifact_id: Optional[UUIDFilter] = None

    generated_by: Optional[UUIDFilter] = None
    owner: Optional[UUIDFilter] = None
