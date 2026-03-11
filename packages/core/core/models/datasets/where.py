from __future__ import annotations
from typing import Optional

from pydantic import Field
from uuid import UUID

from core.models.datasets.artifact_type import ArtifactType
from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter
from core.utils.filters.field_filter import EnumFilter, StringFilter, UUIDFilter, DateTimeFilter, NumberFilter


class DatasetsWhere(BaseUniqueWhere):
    id: UUID = Field(..., description="The unique identifier of the dataset")


class DatasetsFilter(BaseFilter):
    owner_id: Optional[UUIDFilter] = None
    deleted_at: Optional[DateTimeFilter] = None
    name: Optional[StringFilter] = None
    description: Optional[StringFilter] = None
    versions: Optional[DatasetVersionsFilter] = None


class DatasetVersionsWhere(BaseUniqueWhere):
    id: Optional[UUID] = None
    dataset_id: Optional[UUID] = None
    version: Optional[int] = None
    is_latest: Optional[bool] = None


class DatasetVersionsFilter(BaseFilter):
    dataset_id: Optional[UUIDFilter] = None
    artifacts: Optional[DatasetArtifactVersionsFilter] = None


class DatasetArtifactsWhere(BaseUniqueWhere):
    id: Optional[UUID] = None
    dataset_id: Optional[UUID] = None
    checksum: Optional[str] = None


class DatasetArtifactsFilter(BaseFilter):
    dataset_id: Optional[UUIDFilter] = None
    size_in_bytes: Optional[NumberFilter[int]] = None
    checksum: Optional[StringFilter] = None


class DatasetArtifactVersionsWhere(BaseUniqueWhere):
    id: UUID = Field(...,
                     description="The unique identifier of the dataset artifact version")


class DatasetArtifactVersionsFilter(BaseFilter):
    dataset_artifact_id: Optional[UUIDFilter] = None
    artifact_type: Optional[EnumFilter[ArtifactType]] = None
    dataset_artifact: Optional[DatasetArtifactsFilter] = None
