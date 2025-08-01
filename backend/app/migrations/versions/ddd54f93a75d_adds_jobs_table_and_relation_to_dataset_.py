"""Adds jobs table and relation to Dataset table

Revision ID: ddd54f93a75d
Revises: 5901ccbb135f
Create Date: 2025-08-01 19:50:36.192849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ddd54f93a75d'
down_revision: Union[str, Sequence[str], None] = '5901ccbb135f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("jobs",
                    sa.Column("id", sa.UUID(),
                              primary_key=True, nullable=False),
                    sa.Column("description", sa.String(
                        length=255), nullable=False),
                    sa.Column("file_name", sa.String(
                        length=255), nullable=False),
                    sa.Column("dataset_id", sa.UUID(), sa.ForeignKey(
                        "datasets.id"), nullable=False),
                    sa.Column("generations", sa.Integer(),
                              nullable=False, server_default="100"),
                    sa.Column("population_size", sa.Integer(),
                              nullable=False, server_default="100"),
                    sa.Column("max_expression_size", sa.Integer(),
                              nullable=False, server_default="15"),
                    sa.Column("tournament_size", sa.Integer(),
                              nullable=False, server_default="3"),
                    sa.Column("crossover_probability", sa.Float(),
                              nullable=False, server_default="0.9"),
                    sa.Column("mutation_probability", sa.Float(),
                              nullable=False, server_default="0.3"),
                    sa.Column("non_terminals", postgresql.ARRAY(sa.String()), nullable=False,
                              server_default=sa.text("ARRAY['add', 'sub', 'mul', 'div']")),
                    sa.Column("loss_function", sa.Enum("MSE", "Gaussian", "Bernoulli",
                                                       "Poisson", name="lossfunction"), nullable=False, server_default="MSE"),
                    sa.Column("max_optimization_iterations", sa.Integer(),
                              nullable=False, server_default="50"),
                    sa.Column("max_optimization_restarts", sa.Integer(),
                              nullable=False, server_default="2"),
                    sa.Column("parameter_count", sa.Integer(),
                              nullable=False, server_default="-1"),
                    sa.Column("split", sa.Integer(),
                              nullable=False, server_default="1"),
                    sa.Column("simplify", sa.Boolean(),
                              nullable=False, server_default="false"),
                    sa.Column("created_at", postgresql.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column("updated_at", postgresql.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.ForeignKeyConstraint(
                        ["dataset_id"],
                        ["datasets.id"],
                        name=op.f("fk_jobs_dataset_id_datasets"),
                        ondelete="CASCADE"
                    ),
                    sa.PrimaryKeyConstraint("id", name=op.f("pk_jobs")),
                    sa.UniqueConstraint(
                        "file_name", name=op.f("uq_jobs_file_name"))
                    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("jobs")
