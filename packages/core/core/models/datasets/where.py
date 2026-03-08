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
    id: UUID = Field(...,
                     description="The unique identifier of the dataset version")


class DatasetVersionsFilter(BaseFilter):
    dataset_id: Optional[UUIDFilter] = Field(
        None, description="The unique identifier of the dataset associated with the dataset version")


class DatasetArtifactsWhere(BaseUniqueWhere):
    id: UUID = Field(...,
                     description="The unique identifier of the dataset artifact")


class DatasetArtifactsFilter(BaseFilter):
    dataset_version_id: Optional[UUIDFilter] = Field(
        None, description="The unique identifier of the dataset version associated with the dataset artifact")
