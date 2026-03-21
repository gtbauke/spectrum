from __future__ import annotations

from uuid import UUID
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from core.repositories.auth import RefreshToken

from db.common.base.mutable import MutableBase


class RefreshTokenORM(MutableBase):
    __tablename__ = "refresh_tokens"

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
    )

    owner_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("owners.id", ondelete="CASCADE"),
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
            owner_id=self.owner_id,
        )

    @classmethod
    def from_domain(cls, domain_obj: RefreshToken) -> RefreshTokenORM:
        return cls(
            id=domain_obj.id,
            user_id=domain_obj.user_id,
            token_hash=domain_obj.token_hash,
            expires_at=domain_obj.expires_at,
            revoked=domain_obj.revoked,
            created_at=domain_obj.created_at,
            updated_at=domain_obj.updated_at,
            owner_id=domain_obj.owner_id,
        )
