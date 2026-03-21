from pydantic import Field
from uuid import UUID
from datetime import datetime

from core.features.base import BaseMutableDomainModel

from .artifact import Artifact


class Dataset(BaseMutableDomainModel):
    name: str = Field(..., description="The name of the dataset")

    description: str = Field(..., description="The description of the dataset")

    owner_id: UUID = Field(...,
                           description="The ID of the user who owns the dataset")

    artifacts: list[Artifact] = Field(
        [], description="The artifacts of the dataset")
