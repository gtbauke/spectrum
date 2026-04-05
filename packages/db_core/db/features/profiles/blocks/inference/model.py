from uuid import UUID
from sqlalchemy import ForeignKey, String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

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


class InferenceResultORM(ImmutableBase):
    __tablename__ = "inference_results"

    run_id: Mapped[UUID] = mapped_column(
        ForeignKey("inference_runs.id", ondelete="CASCADE"),
        nullable=False
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
