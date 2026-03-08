from uuid import UUID
from fastapi import HTTPException, status


class ArtifactDoesNotBelongToDataset(HTTPException):
    def __init__(self, artifact_id: UUID, dataset_id: UUID):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Artifact with id {artifact_id} does not belong to dataset with id {dataset_id}",
        )
