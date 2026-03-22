from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from sqlalchemy import (
    String,
    DateTime,
)

from db.common.base.mutable import MutableBase

if TYPE_CHECKING:
    from db.features.datasets.model import DatasetORM
    from db.features.profiles.model import ProfileORM


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


class UserORM(MutableBase):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True)

    datasets: Mapped[list["DatasetORM"]] = relationship(
        "DatasetORM",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    profiles: Mapped[list["ProfileORM"]] = relationship(
        "ProfileORM",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
