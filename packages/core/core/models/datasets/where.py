from typing import Optional

from pydantic import Field
from uuid import UUID

from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter
from core.utils.filters.field_filter import UUIDFilter, DateTimeFilter


class DatasetsWhere(BaseUniqueWhere):
    id: UUID = Field(..., description="The unique identifier of the dataset")


class DatasetsFilter(BaseFilter):
    owner_id: Optional[UUIDFilter] = Field(
        None, description="The unique identifier of the owner associated with the dataset")

    deleted_at: Optional[DateTimeFilter] = Field(
        None, description="The timestamp when the dataset was deleted. Null if not deleted")


class DatasetVersionsWhere(BaseUniqueWhere):
    id: Optional[UUID] = None
    dataset_id: Optional[UUID] = None
    version: Optional[int] = None


class DatasetVersionsFilter(BaseFilter):
    dataset_id: Optional[UUIDFilter] = Field(
        None, description="The unique identifier of the dataset associated with the dataset version")


class DatasetArtifactsWhere(BaseUniqueWhere):
    id: Optional[UUID] = None
    dataset_id: Optional[UUID] = None
    checksum: Optional[str] = None


class DatasetArtifactsFilter(BaseFilter):
    dataset_id: Optional[UUIDFilter] = Field(
        None, description="The unique identifier of the dataset associated with the dataset artifact")


class DatasetArtifactVersionsWhere(BaseUniqueWhere):
    id: UUID = Field(...,
                     description="The unique identifier of the dataset artifact version")


class DatasetArtifactVersionsFilter(BaseFilter):
    dataset_artifact_id: Optional[UUIDFilter] = Field(
        None, description="The unique identifier of the dataset artifact associated with the dataset artifact version")
