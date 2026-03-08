from pydantic import BaseModel, Field

from core.models.datasets.dataset import Dataset
from core.models.datasets.dataset_artifact import DatasetArtifact
from core.models.datasets.dataset_version import DatasetVersion


class CreateDatasetResult(BaseModel):
    dataset: Dataset = Field(..., description="The created dataset")
    dataset_version: DatasetVersion = Field(...,
                                            description="The created dataset version")
    dataset_artifact: DatasetArtifact = Field(
        ..., description="The created dataset artifact")
