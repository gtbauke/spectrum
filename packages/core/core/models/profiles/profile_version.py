from uuid import UUID
from pydantic import Field
from typing import TYPE_CHECKING, Optional

from core.models.base import BaseImmutableVersionedDomainModel


if TYPE_CHECKING:
    from core.models.profiles.profile import Profile
    from core.models.profiles.profile_dataset_association import ProfileDatasetAssociation


class ProfileVersion(BaseImmutableVersionedDomainModel):
    profile_id: UUID = Field(...,
                             description="The ID of the profile this version belongs to")

    profile: Optional["Profile"] = Field(...,
                                         description="The profile this version belongs to")

    datasets: list[ProfileDatasetAssociation] = Field(
        ..., description="The datasets associated with this profile version")
