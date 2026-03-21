from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from sqlalchemy import (
    String,
    DateTime,
)

from db.common.base.mutable import MutableBase

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

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True)
