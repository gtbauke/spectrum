from __future__ import annotations

from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Boolean, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from db.common.base.mutable import MutableBase
from core.features.profiles.jobs.loss_function import LossFunction

if TYPE_CHECKING:
    from db.features.profiles.jobs.runs.model import RunORM
    from db.features.profiles.models.model import ModelORM
    from db.features.profiles.model import ProfileORM


class JobORM(MutableBase):
    __tablename__ = "jobs"

    name: Mapped[str] = mapped_column(String, nullable=False)
    profile_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)
    runs_against: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("datasets.id"), nullable=False)

    generations: Mapped[int] = mapped_column(Integer, nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=False)
    max_size: Mapped[int] = mapped_column(Integer, nullable=False)
    number_of_tournaments: Mapped[int] = mapped_column(Integer, nullable=False)

    crossover_probability: Mapped[float] = mapped_column(Float, nullable=False)
    mutation_probability: Mapped[float] = mapped_column(Float, nullable=False)

    non_terminals: Mapped[str] = mapped_column(String, nullable=False)
    loss: Mapped[LossFunction] = mapped_column(
        Enum(LossFunction), nullable=False)

    optimization_iterations: Mapped[int] = mapped_column(
        Integer, nullable=False)
    optimization_repeats: Mapped[int] = mapped_column(Integer, nullable=False)
    max_param_count: Mapped[int] = mapped_column(Integer, nullable=False)
    split: Mapped[int] = mapped_column(Integer, nullable=False)
    simplify: Mapped[bool] = mapped_column(Boolean, nullable=False)

    active_group_by_columns: Mapped[str] = mapped_column(String, nullable=True)
    post_processing_type: Mapped[str] = mapped_column(String, nullable=True)

    runs: Mapped[list["RunORM"]] = relationship(
        "RunORM",
        back_populates="job",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="RunORM.timestamp",
    )

    models: Mapped[list["ModelORM"]] = relationship(
        "ModelORM",
        back_populates="job",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="ModelORM.created_at",
    )

    profile: Mapped["ProfileORM"] = relationship(
        "ProfileORM",
        back_populates="jobs",
        lazy="selectin",
        uselist=False,
    )
