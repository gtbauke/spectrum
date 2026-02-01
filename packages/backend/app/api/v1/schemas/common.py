from pydantic import BaseModel
from uuid import UUID


class IdResponse(BaseModel):
    id: UUID
