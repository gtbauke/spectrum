from uuid import UUID

from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter
from core.utils.filters.field_filter import (
    EnumFilter, NumberFilter, StringFilter, UUIDFilter)

from .artifact_role import ArtifactRole
from .visibility import DatasetVisibility


class ArtifactWhere(BaseUniqueWhere):
    id: UUID


class ArtifactFilter(BaseFilter):
    dataset_id: UUIDFilter | None = None
    checksum: StringFilter | None = None
    size_in_bytes: NumberFilter[int] | None = None
    path: StringFilter | None = None
    role: EnumFilter[ArtifactRole] | None = None


class DatasetWhere(BaseUniqueWhere):
    id: UUID


class DatasetFilter(BaseFilter):
    name: StringFilter | None = None
    description: StringFilter | None = None
    owner_id: UUIDFilter | None = None
    visibility: EnumFilter[DatasetVisibility] | None = None
    artifacts: ArtifactFilter | None = None
