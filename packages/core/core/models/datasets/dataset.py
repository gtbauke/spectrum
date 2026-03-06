from datetime import datetime, timezone
from typing import Optional

from pydantic import Field
from uuid import UUID, uuid4

from core.models.base import BaseTimestampDomainModel


class Dataset(BaseTimestampDomainModel):
    name: str = Field(..., description="The name of the dataset")

    description: Optional[str] = Field(
        None, description="A brief description of the dataset")

    owner_id: UUID = Field(...,
                           description="The ID of the user who owns the dataset")

    @classmethod
    def new(
        cls,
        *,
        name: str,
        description: Optional[str],
        owner_id: UUID,
    ):
        return cls(
            id=uuid4(),
            name=name,
            description=description,
            owner_id=owner_id,
            timestamp=datetime.now(timezone.utc)
        )
