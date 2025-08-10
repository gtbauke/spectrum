"""Creates Job Results table

Revision ID: 24d0484cd9fd
Revises: 0e93ef898493
Create Date: 2025-08-10 00:20:58.278422

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24d0484cd9fd'
down_revision: Union[str, Sequence[str], None] = '0e93ef898493'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "job_results",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("job_id", sa.UUID(), nullable=False),
        sa.Column("job_run_id", sa.UUID(), nullable=False),

        sa.Column("expression_id", sa.Integer(), nullable=False),
        sa.Column("expression", sa.String(), nullable=False),
        sa.Column("numpy_expression", sa.String(), nullable=False),
        sa.Column("latex_expression", sa.String(), nullable=False),
        sa.Column("fitness", sa.Float(), nullable=False),
        sa.Column("parameters", sa.JSON(), nullable=False),
        sa.Column("size", sa.Integer(), nullable=False),
        sa.Column("dl", sa.Float(), nullable=False),

        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),

        sa.PrimaryKeyConstraint("id", name=op.f("pk_job_results")),
        sa.ForeignKeyConstraint(
            ["job_id"],
            ["jobs.id"],
            name=op.f("fk_job_results_job_id_jobs"),
            ondelete="CASCADE",
            onupdate="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["job_run_id"],
            ["job_runs.id"],
            name=op.f("fk_job_results_job_run_id_job_runs"),
            ondelete="CASCADE",
            onupdate="CASCADE"
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("job_results")
