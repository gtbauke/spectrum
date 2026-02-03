from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class Model(BaseModel):
    id: UUID

    name: str
    dataset_id: UUID
    version: int

    created_at: datetime
    updated_at: datetime
