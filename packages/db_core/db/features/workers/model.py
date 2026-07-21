from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func

from db.common.base.root import RootBase


class WorkerHeartbeatORM(RootBase):
    """Stores periodic heartbeat data from each worker instance.

    Uses worker_id as the primary key (not a UUID) because worker IDs
    are deterministic strings like ``training-hostname-12345``.
    """

    __tablename__ = "worker_heartbeats"

    worker_id: Mapped[str] = mapped_column(
        String, primary_key=True, nullable=False,
    )

    worker_type: Mapped[str] = mapped_column(
        String, nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String, nullable=False, default="idle",
    )

    current_task: Mapped[str | None] = mapped_column(
        String, nullable=True,
    )

    task_started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
    )

    last_heartbeat: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(),
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(),
    )
