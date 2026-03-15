from typing import Optional
from uuid import UUID

from core.utils.filters.field_filter import BooleanFilter, StringFilter, UUIDFilter
from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter


class JobWhere(BaseUniqueWhere):
    id: Optional[UUID] = None
    profile_version_id: Optional[UUID] = None
    owner_id: Optional[UUID] = None


class JobFilter(BaseFilter):
    owner_id: Optional[UUIDFilter] = None
    profile_version_id: Optional[UUIDFilter] = None
    versions: Optional["JobVersionFilter"] = None


class JobVersionWhere(BaseUniqueWhere):
    id: Optional[UUID] = None
    job_id: Optional[UUID] = None
    is_latest: Optional[bool] = None


class JobVersionFilter(BaseFilter):
    name: Optional[StringFilter] = None
    profile_version_id: Optional[UUIDFilter] = None
    is_latest: Optional[BooleanFilter] = None
