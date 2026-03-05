from uuid import UUID

from fastapi import HTTPException, status


class OwnerNotFound(HTTPException):
    def __init__(self, entity_id: UUID):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner associated with entity id {entity_id} not found".format(
                entity_id=entity_id)
        )
