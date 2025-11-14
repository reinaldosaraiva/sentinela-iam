"""Add missing columns to applications table

Revision ID: 002_add_missing_columns
Revises: 001_create_tables
Create Date: 2025-11-13 10:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '002_add_missing_columns'
down_revision: Union[str, None] = '001_create_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add missing columns to applications table
    op.add_column('applications', sa.Column('logo_url', sa.String(length=500), nullable=True))
    op.add_column('applications', sa.Column('website_url', sa.String(length=500), nullable=True))
    op.add_column('applications', sa.Column('environment', sa.String(length=20), nullable=False, server_default='development'))
    op.add_column('applications', sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True))
    
    # Convert id column to UUID
    op.execute('ALTER TABLE applications DROP CONSTRAINT applications_pkey')
    op.drop_column('applications', 'id')
    op.add_column('applications', sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')))
    op.execute('ALTER TABLE applications ADD PRIMARY KEY (id)')


def downgrade() -> None:
    # Remove added columns
    op.drop_column('applications', 'created_by')
    op.drop_column('applications', 'environment')
    op.drop_column('applications', 'website_url')
    op.drop_column('applications', 'logo_url')
    
    # Convert id back to integer
    op.execute('ALTER TABLE applications DROP CONSTRAINT applications_pkey')
    op.drop_column('applications', 'id')
    op.add_column('applications', sa.Column('id', sa.Integer(), nullable=False))
    op.execute('ALTER TABLE applications ADD PRIMARY KEY (id)')