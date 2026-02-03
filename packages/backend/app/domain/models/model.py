from __future__ import annotations

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

    @classmethod
    def create(cls, *, name: str, dataset_id: UUID, version: int) -> Model:
        now = datetime.now()

        return cls(
            id=UUID(),
            name=name,
            dataset_id=dataset_id,
            version=version,
            created_at=now,
            updated_at=now,
        )
