from uuid import UUID

from pydantic import BaseModel, Field

from app.features.users.responses.user_details import UserDetails
from core.models.owners.owner_type import OwnerType


class OwnerDetails(BaseModel):
    model_config = {
        "from_attributes": True,
    }

    id: UUID = Field(..., description="ID of the owner")
    type: OwnerType = Field(..., description="Type of the owner")

    details: UserDetails = Field(
        ...,
        description="Details of the entity associated with this owner entity"
    )
