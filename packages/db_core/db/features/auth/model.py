from __future__ import annotations

from uuid import UUID
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from db.common.base.mutable import MutableBase


class RefreshTokenORM(MutableBase):
    __tablename__ = "refresh_tokens"

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
    )

    token_hash: Mapped[str] = mapped_column(String, nullable=False)

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False)

    revoked: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False)

    __table_args__ = (
        Index("ix_refresh_tokens_token_hash", "token_hash"),
    )
