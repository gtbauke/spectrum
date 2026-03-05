from __future__ import annotations
from typing import Optional

from pydantic import BaseModel, Field, model_validator
from uuid import UUID

from core.models.owners.owner_type import OwnerType
from core.models.owners.errors.invalid_owner_attachment import InvalidOwnerAttachment


class CreateOwnerDTO(BaseModel):
    owner_type: OwnerType = Field(..., description="The type of the owner")

    user_id: Optional[UUID] = Field(
        ..., description="The ID of the user associated with the owner, if applicable")

    @model_validator(mode="after")
    def validate_owner_type(self):
        if self.owner_type == OwnerType.USER and self.user_id is None:
            raise InvalidOwnerAttachment(OwnerType.USER, None)

        return self

    @classmethod
    def user(cls, user_id: UUID) -> CreateOwnerDTO:
        return cls(owner_type=OwnerType.USER, user_id=user_id)
