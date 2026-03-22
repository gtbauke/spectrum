from pydantic import BaseModel, Field, EmailStr, SecretStr, field_validator


class UpdateUserDto(BaseModel):
    first_name: str | None = Field(None, description="The user's first name")
    last_name: str | None = Field(None, description="The user's last name")
    email: EmailStr | None = Field(
        None, description="The user's email address")
    password: SecretStr | None = Field(None, description="The user's password")

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
