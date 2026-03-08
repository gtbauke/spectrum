from uuid import UUID
from enum import StrEnum
from pydantic import BaseModel, Field

from core.models.datasets.dataset_artifact_version import DatasetArtifactVersion
from core.models.datasets.artifact_type import ArtifactType


class AssociationErrorReason(StrEnum):
    ARTIFACT_DOES_NOT_BELONG_TO_DATASET = "ARTIFACT_DOES_NOT_BELONG_TO_DATASET"
    ARTIFACT_DOES_NOT_EXIST = "ARTIFACT_DOES_NOT_EXIST"
    OTHER = "OTHER"


class AssociationError(BaseModel):
    dataset_version_id: UUID = Field(
        ...,
        description="The ID of the dataset version to which the artifact belongs"
    )

    artifact_id: UUID = Field(
        ...,
        description="The ID of the artifact that failed to associate with the dataset version"
    )

    artifact_type: ArtifactType = Field(
        ...,
        description="The type of the artifact that failed to associate with the dataset version"
    )

    error_reason: AssociationErrorReason = Field(
        ...,
        description="The reason for the association failure"
    )


class BulkCreateAssociationResult(BaseModel):
    associated: list[DatasetArtifactVersion] = Field(
        ...,
        description="List of successfully associated artifacts with the dataset version",
    )

    errors: list[AssociationError] = Field(
        ...,
        description="List of errors that occurred during the association process",
    )
