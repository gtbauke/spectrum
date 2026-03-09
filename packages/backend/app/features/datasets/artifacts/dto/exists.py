from uuid import UUID
from pydantic import BaseModel, Field


class DatasetArtifactExistsDTO(BaseModel):
    dataset_id: UUID = Field(...,
                             description="The unique identifier of the dataset")
    checksum: str = Field(
        ..., description="The checksum of the dataset artifact, used for integrity verification")
