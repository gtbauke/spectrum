from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import Field, EmailStr, SecretStr
from ..base import BaseMutableDomainModel


class User(BaseMutableDomainModel):
    first_name: str = Field(..., description="The user's first name")

    last_name: str = Field(..., description="The user's last name")

    email: EmailStr = Field(..., description="The user's email address")

    password_hash: SecretStr = Field(...,
                                     description="The hashed password of the user")

    deleted_at: Optional[datetime] = Field(
        None, description="The timestamp when the user was deleted, if applicable")

    @classmethod
    def new(
        cls,
        *,
        first_name: str,
        last_name: str,
        email: EmailStr,
        password_hash: SecretStr,
    ):
        return cls(
            id=uuid4(),
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=password_hash,
            deleted_at=None,
        )
