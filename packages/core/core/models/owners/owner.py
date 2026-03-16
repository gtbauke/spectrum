from __future__ import annotations

from pydantic import Field, model_validator
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone

from core.models.base import BaseImmutableVersionedDomainModel
from core.models.owners.errors.invalid_owner_attachment import InvalidOwnerAttachment
from core.models.owners.owner_type import OwnerType
from core.models.users.user import User


class Owner(BaseImmutableVersionedDomainModel):
    """
    The `Owner` class represents an entity that can own resources within the system. It is designed to be flexible and can represent different types of owners, such as users, teams, or organizations.

    Properties:
    - `owner_type`: An enumeration that specifies the type of owner (e.g., USER, TEAM, ORGANIZATION).
    """
    owner_type: OwnerType = Field(
        ..., description="The type of the owner (e.g., USER, TEAM, ORGANIZATION)")

    user_id: Optional[UUID] = Field(
        None, description="The ID of the user if the owner is a USER")

    deleted_at: Optional[datetime] = Field(
        None, description="The timestamp when the owner was deleted, if applicable")

    user: Optional[User] = Field(
        None, description="The user associated with this owner entity (if applicable)")

    @model_validator(mode="after")
    def validate_owner_identity(self):
        if self.owner_type == OwnerType.USER and not self.user_id:
            raise InvalidOwnerAttachment(
                owner_type=OwnerType.USER, received=None)

        return self

    @classmethod
    def new_user(cls, *, user_id: UUID, user: Optional[User] = None) -> Owner:
        return cls(
            id=uuid4(),
            timestamp=datetime.now(timezone.utc),
            version=1,
            owner_type=OwnerType.USER,
            user_id=user_id,
            deleted_at=None,
            is_latest=True,
            user=user,
        )
