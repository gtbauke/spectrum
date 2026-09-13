from uuid import UUID

from app.core.utils.filters.field_filter import (
    DateTimeFilter, EnumFilter, StringFilter, UUIDFilter)
from app.core.utils.where import BaseUniqueWhere
from app.core.utils.filters.base import BaseFilter
from app.features.datasets.domain.where import DatasetFilter

from .profile_mode import ProfileMode
from app.features.profiles.jobs.domain.where import JobFilter
from app.features.profiles.models.domain.where import ModelFilter
from app.features.profiles.blocks.domain.where import BlockFilter


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
