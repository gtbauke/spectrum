"""creates datasets table

Revision ID: f44974654494
Revises: 
Create Date: 2025-07-19 21:35:13.226408

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects.postgresql import UUID

import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = 'f44974654494'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'datasets',
        sa.Column('id', UUID(as_uuid=True), primary_key=True,
                  nullable=False, default=uuid.uuid4),
        sa.Column('name', sa.String(255), nullable=False, unique=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(
        ), onupdate=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('datasets')
