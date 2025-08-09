"""Creates Jobs Run table

Revision ID: 0e93ef898493
Revises: ddd54f93a75d
Create Date: 2025-08-02 00:34:57.927515

"""
import sqlalchemy as sa

from typing import Sequence, Union
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '0e93ef898493'
down_revision: Union[str, Sequence[str], None] = 'ddd54f93a75d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "job_runs",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("job_id", sa.UUID(), sa.ForeignKey(
            "jobs.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
        sa.Column("status", sa.Enum("PENDING", "RUNNING", "COMPLETED", "FAILED", "CANCELLED",
                                    name="jobstatus"), nullable=False, server_default="PENDING"),
        sa.Column("created_at", postgresql.TIMESTAMP(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column("updated_at", postgresql.TIMESTAMP(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column("finished_at", postgresql.TIMESTAMP(timezone=True),
                  nullable=True, server_default=None),
        sa.PrimaryKeyConstraint("id", name="pk_jobs_run_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("jobs_run")
    op.execute("DROP TYPE IF EXISTS jobstatus")
