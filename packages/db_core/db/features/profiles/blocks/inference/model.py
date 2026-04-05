from typing import Any
from uuid import UUID
from sqlalchemy import ForeignKey, String, Integer, Float, Enum, UniqueConstraint, Index, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, declared_attr
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID

from core.features.profiles.blocks.inference.inference_run import InferenceRunStatus
from db.common.base.immutable import ImmutableBase, ImmutableVersionedBase


class InferenceRunORM(ImmutableVersionedBase):
    __tablename__ = "inference_runs"

    block_id: Mapped[UUID] = mapped_column(
        ForeignKey("blocks.id", ondelete="CASCADE"),
        nullable=False
    )

    profile_id: Mapped[UUID] = mapped_column(
        ForeignKey("profiles.id", ondelete="CASCADE"),
        nullable=False
    )

    query: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    status: Mapped[InferenceRunStatus] = mapped_column(
        Enum(InferenceRunStatus),
        default=InferenceRunStatus.PENDING,
        nullable=False
    )

    execution_time_ms: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    error: Mapped[str] = mapped_column(
        String,
        nullable=True
    )


class InferenceResultORM(ImmutableBase):
    __tablename__ = "inference_results"

    run_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
    )

    run_version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    expression: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    dl: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

    fitness: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

    latex: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    numpy: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    parameters: Mapped[dict[str, float]] = mapped_column(
        JSONB,
        nullable=True
    )

    size: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    @declared_attr.directive
    def __table_args__(cls) -> Any:
        return (
            UniqueConstraint("id", name=f"uq_{cls.__tablename__}_id"),
            Index(f"idx_{cls.__tablename__}_timestamp", "timestamp"),
            ForeignKeyConstraint(
                ["run_id", "run_version"],
                ["inference_runs.id", "inference_runs.version"],
                ondelete="CASCADE"
            ),
        )
