from datetime import datetime, timezone
from typing import Optional

from pydantic import Field
from uuid import UUID, uuid4

from core.models.base import BaseMutableDomainModel


class Dataset(BaseMutableDomainModel):
    name: str = Field(..., description="The name of the dataset")

    description: Optional[str] = Field(
        None, description="A brief description of the dataset")

    owner_id: UUID = Field(...,
                           description="The ID of the user who owns the dataset")

    deleted_at: Optional[datetime] = Field(
        None, description="The timestamp when the dataset was deleted, if applicable"
    )

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
            deleted_at=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
