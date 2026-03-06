from core.utils.where import BaseUniqueWhere

from pydantic import Field
from uuid import UUID


class DatasetsWhere(BaseUniqueWhere):
    id: UUID = Field(..., description="The unique identifier of the dataset")


class DatasetVersionsWhere(BaseUniqueWhere):
    id: UUID = Field(...,
                     description="The unique identifier of the dataset version")


class DatasetArtifactsWhere(BaseUniqueWhere):
    id: UUID = Field(...,
                     description="The unique identifier of the dataset artifact")
