from uuid import UUID

from core.utils.filters.field_filter import (
    DateTimeFilter, EnumFilter, StringFilter, UUIDFilter)
from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter
from core.features.datasets.where import DatasetFilter

from .profile_mode import ProfileMode
from .jobs.where import JobFilter
from .models.where import ModelFilter
from .blocks.where import BlockFilter


class ProfileWhere(BaseUniqueWhere):
    id: UUID


class ProfileFilter(BaseFilter):
    id: UUIDFilter | None = None
    created_at: DateTimeFilter | None = None
    updated_at: DateTimeFilter | None = None
    name: StringFilter | None = None
    description: StringFilter | None = None
    owner_id: UUIDFilter | None = None
    mode: EnumFilter[ProfileMode] | None = None
    datasets: DatasetFilter | None = None
    jobs: JobFilter | None = None
    models: ModelFilter | None = None
    blocks: BlockFilter | None = None
