from uuid import UUID
from pydantic import Field
from typing import Optional

from core.models.base import BaseImmutableDomainModel
from core.models.profiles.profile_dataset_role import ProfileDatasetRole

from core.models.datasets.dataset_version import DatasetVersion


class ProfileDatasetAssociation(BaseImmutableDomainModel):
    profile_version_id: UUID = Field(
        default=..., description="The ID of the profile version this association belongs to")

    dataset_version_id: UUID = Field(
        ..., description="The ID of the dataset version this association belongs to")

    role: ProfileDatasetRole = Field(
        ..., description="The role of the dataset in the profile version")

    dataset_version: Optional[DatasetVersion] = Field(
        None, description="The dataset version this association belongs to")
