from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import SecretStr

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from sqlalchemy import (
    String,
    DateTime,
)

from db.base import Base
from core.models.users.user import User


class UserORM(Base):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True)

    @classmethod
    def from_domain(cls, domain_user: User) -> UserORM:
        return cls(
            id=domain_user.id,
            first_name=domain_user.first_name,
            last_name=domain_user.last_name,
            email=domain_user.email,
            password_hash=domain_user.password_hash.get_secret_value(),
            created_at=domain_user.created_at,
            updated_at=domain_user.updated_at,
            deleted_at=domain_user.deleted_at,
        )

    def to_domain(self) -> User:
        return User(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password_hash=SecretStr(self.password_hash),
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
        )
