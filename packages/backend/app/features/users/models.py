from __future__ import annotations

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import SecretStr

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from sqlalchemy import (
    String,
    DateTime,
)

from db.base import Base
from core.models.users.user import User

if TYPE_CHECKING:
    from app.features.owners.models import OwnerORM

# TODO: enable email reuse after soft deletion using where-like unique constraints
# we should also change the logic of retrieving a unique user to search only for active users (deleted_at is None)
# __table_args__ = (
#     Index(
#         "uq_users_email_active",
#         "email",
#         unique=True,
#         postgresql_where=(deleted_at.is_(None)),
#     ),
# )


class UserORM(Base):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True)

    owner: Mapped[OwnerORM] = relationship(
        "OwnerORM",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    @classmethod
    def from_domain(cls, domain_obj: User) -> UserORM:
        return cls(
            id=domain_obj.id,
            first_name=domain_obj.first_name,
            last_name=domain_obj.last_name,
            email=domain_obj.email,
            password_hash=domain_obj.password_hash.get_secret_value(),
            created_at=domain_obj.created_at,
            updated_at=domain_obj.updated_at,
            deleted_at=domain_obj.deleted_at,
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
