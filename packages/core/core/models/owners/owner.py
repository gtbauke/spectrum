from pydantic import Field, model_validator
from typing import Optional
from uuid import UUID

from core.models.base import BaseImmutableDomainModel
from core.models.owners.errors.invalid_owner_attachment import InvalidOwnerAttachment
from core.models.owners.owner_type import OwnerType


class Owner(BaseImmutableDomainModel):
    """
    The `Owner` class represents an entity that can own resources within the system. It is designed to be flexible and can represent different types of owners, such as users, teams, or organizations.

    Properties:
    - `owner_type`: An enumeration that specifies the type of owner (e.g., USER, TEAM, ORGANIZATION).
    """
    owner_type: OwnerType = Field(
        ..., description="The type of the owner (e.g., USER, TEAM, ORGANIZATION)")

    user_id: Optional[UUID] = Field(
        None, description="The ID of the user if the owner is a USER")

    @model_validator(mode="after")
    def validate_owner_identity(self):
        if self.owner_type == OwnerType.USER and not self.user_id:
            raise InvalidOwnerAttachment(
                owner_type=OwnerType.USER, received=None)

        return self
