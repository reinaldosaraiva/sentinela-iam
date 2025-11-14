"""Add missing columns to resources and actions tables

Revision ID: 005_add_missing_columns_resources_actions
Revises: 002_add_missing_columns_simple
Create Date: 2025-11-13 11:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '005_add_missing_columns_resources_actions'
down_revision: Union[str, None] = '002_add_missing_columns_simple'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add missing columns to resources table
    op.add_column('resources', sa.Column('created_by', sa.String(length=100), nullable=True))
    
    # Add missing columns to actions table
    op.add_column('actions', sa.Column('created_by', sa.String(length=100), nullable=True))


def downgrade() -> None:
    # Remove added columns
    op.drop_column('actions', 'created_by')
    op.drop_column('resources', 'created_by')