from uuid import UUID
from fastapi import HTTPException, status


class ArtifactNotFound(HTTPException):
    def __init__(self, artifact_id: UUID):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Artifact with id {artifact_id} not found",
        )
