from uuid import UUID
from pydantic import BaseModel

from app.features.profiles.models import ProfileDatasetRole


class CreateAssociationRouteDTO(BaseModel):
    dataset_version_id: UUID
    role: ProfileDatasetRole


class CreateAssociationDTO(CreateAssociationRouteDTO):
    profile_version_id: UUID
