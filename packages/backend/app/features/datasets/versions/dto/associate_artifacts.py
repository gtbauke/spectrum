from uuid import UUID
from pydantic import BaseModel, Field

from core.models.datasets.artifact_type import ArtifactType


class Association(BaseModel):
    artifact_id: UUID = Field(
        ...,
        description="ID of the artifact to associate with the dataset version."
    )

    artifact_type: ArtifactType = Field(
        ...,
        description="Type of artifact to associate with the dataset version."
    )


class AssociateArtifactsRouteDTO(BaseModel):
    associations: list[Association] = Field(
        ...,
        description="List of associations to be made"
    )


class AssociateArtifactsDTO(AssociateArtifactsRouteDTO):
    dataset_id: UUID = Field(
        ...,
        description="ID of the dataset to which the version belongs."
    )
