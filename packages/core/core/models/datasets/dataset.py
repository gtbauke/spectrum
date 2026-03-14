from datetime import datetime, timezone
from typing import Optional

from pydantic import Field
from uuid import UUID, uuid4

from core.models.base import BaseMutableDomainModel

from .dataset_version import DatasetVersion


class Dataset(BaseMutableDomainModel):
    owner_id: UUID = Field(...,
                           description="The ID of the user who owns the dataset")

    deleted_at: Optional[datetime] = Field(
        None, description="The timestamp when the dataset was deleted, if applicable"
    )

    versions: list[DatasetVersion] = Field(
        ...,
        description="List of versions associated with this dataset"
    )

    @classmethod
    def new(
        cls,
        *,
        owner_id: UUID,
    ):
        return cls(
            id=uuid4(),
            owner_id=owner_id,
            deleted_at=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            versions=[],
        )

    def add_version(self, version: DatasetVersion):
        self.versions.append(version)
