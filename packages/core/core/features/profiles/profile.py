from uuid import UUID
from pydantic import Field
from datetime import datetime

from core.features.base import BaseMutableDomainModel
from core.features.datasets.dataset import Dataset

from .profile_mode import ProfileMode
from .jobs.job import Job
from .models.model import Model
from .blocks.block import Block


class Profile(BaseMutableDomainModel):
    name: str = Field(..., description="The name of the profile")

    description: str = Field(..., description="The description of the profile")

    owner_id: UUID = Field(...,
                           description="The ID of the user who owns the profile")

    mode: ProfileMode = Field(
        ProfileMode.DRAFT, description="The mode of the profile")

    deleted_at: datetime | None = Field(
        None, description="The date and time when the profile was deleted")

    datasets: list[Dataset] = Field(
        [], description="The datasets of the profile")

    jobs: list[Job] = Field(
        [], description="The jobs of the profile")

    models: list[Model] = Field(
        [], description="The models of the profile")

    blocks: list[Block] = Field(
        [], description="The blocks of the profile")
