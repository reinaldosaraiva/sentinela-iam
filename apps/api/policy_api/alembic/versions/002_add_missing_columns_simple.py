"""Add missing columns to applications table (simple version)

Revision ID: 002_add_missing_columns_simple
Revises: 001_create_tables
Create Date: 2025-11-13 10:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002_add_missing_columns_simple'
down_revision: Union[str, None] = '001_create_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add missing columns to applications table
    op.add_column('applications', sa.Column('logo_url', sa.String(length=500), nullable=True))
    op.add_column('applications', sa.Column('website_url', sa.String(length=500), nullable=True))
    op.add_column('applications', sa.Column('environment', sa.String(length=20), nullable=False, server_default='development'))
    op.add_column('applications', sa.Column('created_by', sa.String(length=100), nullable=True))  # Temporarily string instead of UUID


def downgrade() -> None:
    # Remove added columns
    op.drop_column('applications', 'created_by')
    op.drop_column('applications', 'environment')
    op.drop_column('applications', 'website_url')
    op.drop_column('applications', 'logo_url')