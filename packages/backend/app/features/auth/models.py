from __future__ import annotations

from uuid import UUID
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from core.repositories.auth import RefreshToken
from db.base import Base


class RefreshTokenORM(Base):
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

    def to_domain(self) -> RefreshToken:
        return RefreshToken(
            id=self.id,
            user_id=self.user_id,
            token_hash=self.token_hash,
            expires_at=self.expires_at,
            revoked=self.revoked,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain(cls, refresh_token: RefreshToken) -> RefreshTokenORM:
        return cls(
            id=refresh_token.id,
            user_id=refresh_token.user_id,
            token_hash=refresh_token.token_hash,
            expires_at=refresh_token.expires_at,
            revoked=refresh_token.revoked,
            created_at=refresh_token.created_at,
            updated_at=refresh_token.updated_at,
        )
