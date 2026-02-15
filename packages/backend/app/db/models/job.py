from __future__ import annotations

import uuid

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import (DateTime, Enum, func, ForeignKey,
                        Integer, String, Boolean, Float)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.domain.jobs.job_status import JobStatus
from app.domain.jobs.job import Job
from app.domain.jobs.loss_function import LossFunction
from app.domain.jobs.available_functions import AvailableFunctions

if TYPE_CHECKING:
    from app.db.models.dataset import DatasetORM
    from app.db.models.model import ModelORM


class JobORM(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    status: Mapped[JobStatus] = mapped_column(
        Enum(
            JobStatus,
            name="job_status",
        ),
        nullable=False,
        default=JobStatus.PENDING,
    )

    dataset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("datasets.id", ondelete="CASCADE"),
        nullable=False,
    )

    dataset: Mapped["DatasetORM"] = relationship(
        back_populates="jobs",
        lazy="selectin",
    )

    model: Mapped["ModelORM"] = relationship(
        back_populates="job",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now(),
    )

    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    finished_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    generations: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=100,
    )

    population: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=100,
    )

    max_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=15,
    )

    number_of_tournaments: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=3,
    )

    crossover_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.9,
    )

    mutation_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.3,
    )

    non_terminals: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=AvailableFunctions.from_list(
            AvailableFunctions.ADD,
            AvailableFunctions.SUB,
            AvailableFunctions.MUL,
            AvailableFunctions.DIV,
        ),
    )

    loss: Mapped[LossFunction] = mapped_column(
        Enum(
            LossFunction,
            name="loss_function",
        ),
        nullable=False,
        default=LossFunction.MSE,
    )

    optimization_iterations: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=50,
    )

    optimization_repeats: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=2,
    )

    max_param_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=-1,
    )

    split: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    simplify: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    def to_domain(self) -> Job:
        return Job(
            id=self.id,
            status=self.status,
            dataset_id=self.dataset_id,
            created_at=self.created_at,
            started_at=self.started_at,
            finished_at=self.finished_at,
            model=self.model.to_domain() if self.model else None,
            generations=self.generations,
            population=self.population,
            max_size=self.max_size,
            number_of_tournaments=self.number_of_tournaments,
            crossover_probability=self.crossover_probability,
            mutation_probability=self.mutation_probability,
            non_terminals=AvailableFunctions.to_list(self.non_terminals),
            loss=self.loss,
            optimization_iterations=self.optimization_iterations,
            optimization_repeats=self.optimization_repeats,
            max_param_count=self.max_param_count,
            split=self.split,
            simplify=self.simplify,
        )

    @classmethod
    def from_domain(cls, job: Job) -> JobORM:
        return cls(
            id=job.id,
            status=job.status,
            dataset_id=job.dataset_id,
            created_at=job.created_at,
            started_at=job.started_at,
            finished_at=job.finished_at,
            model=ModelORM.from_domain(job.model) if job.model else None,
            generations=job.generations,
            population=job.population,
            max_size=job.max_size,
            number_of_tournaments=job.number_of_tournaments,
            crossover_probability=job.crossover_probability,
            mutation_probability=job.mutation_probability,
            non_terminals=AvailableFunctions.from_list(*job.non_terminals),
            loss=job.loss,
            optimization_iterations=job.optimization_iterations,
            optimization_repeats=job.optimization_repeats,
            max_param_count=job.max_param_count,
            split=job.split,
            simplify=job.simplify,
        )
