from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class UpdateUserDTO(BaseModel):
    first_name: Optional[str] = Field(
        None, description="The first name of the user")

    last_name: Optional[str] = Field(
        None, description="The last name of the user")

    email: Optional[EmailStr] = Field(
        None, description="The email of the user")

    password: Optional[str] = Field(
        None,
        description="The password of the user",
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not any(c.islower() for c in value):
            raise ValueError(
                "Password must contain at least one lowercase letter")

        if not any(c.isupper() for c in value):
            raise ValueError(
                "Password must contain at least one uppercase letter")

        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit")

        if not any(c in "@$!%*?&" for c in value):
            raise ValueError(
                "Password must contain at least one special character (@$!%*?&)"
            )

        return value
