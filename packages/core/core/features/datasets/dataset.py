from pydantic import Field
from uuid import UUID
from datetime import datetime

from core.features.base import BaseMutableDomainModel

from .artifact import Artifact
from .visibility import DatasetVisibility


class Dataset(BaseMutableDomainModel):
    name: str = Field(..., description="The name of the dataset")

    description: str = Field(..., description="The description of the dataset")

    owner_id: UUID = Field(...,
                           description="The ID of the user who owns the dataset")

    artifacts: list[Artifact] = Field(
        [], description="The artifacts of the dataset")

    deleted_at: datetime | None = Field(
        None, description="The timestamp when the dataset was deleted")

    visibility: DatasetVisibility = Field(
        DatasetVisibility.PRIVATE,
        description="Controls who can see and use this dataset",
    )

    @classmethod
    def new(
        cls,
        name: str,
        description: str,
        owner_id: UUID,
        visibility: DatasetVisibility = DatasetVisibility.PRIVATE
    ) -> "Dataset":
        return cls(
            name=name,
            description=description,
            owner_id=owner_id,
            artifacts=[],
            deleted_at=None,
            visibility=visibility
        )
