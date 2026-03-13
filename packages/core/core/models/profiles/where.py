from typing import Optional
from uuid import UUID

from core.models.datasets.where import DatasetVersionsFilter
from core.models.profiles.profile_dataset_role import ProfileDatasetRole
from core.models.profiles.profile_status import ProfileStatus
from core.models.profiles.profile_visibility import ProfileVisibility
from core.utils.filters.field_filter import (
    DateTimeFilter,
    EnumFilter,
    NumberFilter,
    StringFilter,
    UUIDFilter
)
from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter


class ProfileDatasetAssociationWhere(BaseUniqueWhere):
    id: UUID


class ProfileDatasetAssociationFilter(BaseFilter):
    id: Optional[UUIDFilter] = None
    timestamp: Optional[DateTimeFilter] = None
    profile_version_id: Optional[UUIDFilter] = None
    dataset_version_id: Optional[UUIDFilter] = None
    role: Optional[EnumFilter[ProfileDatasetRole]] = None
    dataset_version: Optional[DatasetVersionsFilter] = None


class ProfileVersionWhere(BaseUniqueWhere):
    id: Optional[UUID] = None
    profile_id: Optional[UUID] = None
    version: Optional[int] = None
    is_latest: Optional[bool] = None


class ProfileVersionFilter(BaseFilter):
    id: Optional[UUIDFilter] = None
    name: Optional[StringFilter] = None
    description: Optional[StringFilter] = None
    status: Optional[EnumFilter[ProfileStatus]] = None
    visibility: Optional[EnumFilter[ProfileVisibility]] = None
    profile_id: Optional[UUIDFilter] = None
    version: Optional[NumberFilter[int]] = None
    is_latest: Optional[bool] = None
    timestamp: Optional[DateTimeFilter] = None

    datasets: Optional[ProfileDatasetAssociationFilter] = None


class ProfilesWhere(BaseUniqueWhere):
    id: UUID
    is_latest: Optional[bool] = None


class ProfilesFilter(BaseFilter):
    id: Optional[UUIDFilter] = None
    version: Optional[NumberFilter[int]] = None
    is_latest: Optional[bool] = None
    timestamp: Optional[DateTimeFilter] = None

    owner_id: Optional[UUIDFilter] = None
    versions: Optional[ProfileVersionFilter] = None
