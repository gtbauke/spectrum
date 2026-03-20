from __future__ import annotations

from uuid import UUID
from pydantic import Field
from typing import TYPE_CHECKING, Optional
from datetime import datetime, timezone

from core.models.base import BaseImmutableVersionedDomainModel
from core.models.models.model import Model
from core.models.profiles.profile_status import ProfileStatus
from core.models.profiles.profile_visibility import ProfileVisibility


if TYPE_CHECKING:
    from core.models.profiles.profile_dataset_association import ProfileDatasetAssociation
    from core.models.profiles.profile_block import ProfileBlock


class ProfileVersion(BaseImmutableVersionedDomainModel):
    name: str = Field(..., max_length=255,
                      description="The name of the profile")

    description: Optional[str] = Field(
        None, description="A brief description of the profile")

    status: ProfileStatus = Field(..., description="The status of the profile")

    visibility: ProfileVisibility = Field(...,
                                          description="The visibility of the profile")

    profile_id: UUID = Field(...,
                             description="The ID of the profile this version belongs to")

    datasets: list[ProfileDatasetAssociation] = Field(
        ..., description="The datasets associated with this profile version")

    blocks: list[ProfileBlock] = Field(
        ..., description="The blocks associated with this profile version")

    models: list[Model] = Field(
        ..., description="The models associated with this profile version")

    @classmethod
    def new(
        cls,
        *,
        name: str,
        description: Optional[str],
        visibility: ProfileVisibility,
        profile_id: UUID,
        version: int,
        is_latest: bool,
        blocks: list[ProfileBlock] = [],
        datasets: list[ProfileDatasetAssociation] = [],
        models: list[Model] = [],
    ) -> "ProfileVersion":
        return cls(
            name=name,
            description=description,
            visibility=visibility,
            profile_id=profile_id,
            status=ProfileStatus.ACTIVE,
            datasets=datasets,
            version=version,
            is_latest=is_latest,
            timestamp=datetime.now(timezone.utc),
            blocks=blocks,
            models=models,
        )
