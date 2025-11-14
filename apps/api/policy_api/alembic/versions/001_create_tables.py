"""Create application tables

Revision ID: 001_create_tables
Revises: 
Create Date: 2025-11-13 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_create_tables'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create applications table
    op.create_table('applications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('slug', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_applications_slug'), 'applications', ['slug'], unique=True)
    op.create_index(op.f('ix_applications_status'), 'applications', ['status'], unique=False)

    # Create api_keys table
    op.create_table('api_keys',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('application_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('key_hash', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('last_used_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['application_id'], ['applications.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_api_keys_application_id'), 'api_keys', ['application_id'], unique=False)
    op.create_index(op.f('ix_api_keys_is_active'), 'api_keys', ['is_active'], unique=False)

    # Create resources table
    op.create_table('resources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('application_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('resource_type', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['application_id'], ['applications.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resources_application_id'), 'resources', ['application_id'], unique=False)
    op.create_index(op.f('ix_resources_is_active'), 'resources', ['is_active'], unique=False)
    op.create_index(op.f('ix_resources_resource_type'), 'resources', ['resource_type'], unique=False)

    # Create actions table
    op.create_table('actions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('resource_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('action_type', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['resource_id'], ['resources.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_actions_action_type'), 'actions', ['action_type'], unique=False)
    op.create_index(op.f('ix_actions_is_active'), 'actions', ['is_active'], unique=False)
    op.create_index(op.f('ix_actions_resource_id'), 'actions', ['resource_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_actions_resource_id'), table_name='actions')
    op.drop_index(op.f('ix_actions_is_active'), table_name='actions')
    op.drop_index(op.f('ix_actions_action_type'), table_name='actions')
    op.drop_table('actions')
    op.drop_index(op.f('ix_resources_resource_type'), table_name='resources')
    op.drop_index(op.f('ix_resources_is_active'), table_name='resources')
    op.drop_index(op.f('ix_resources_application_id'), table_name='resources')
    op.drop_table('resources')
    op.drop_index(op.f('ix_api_keys_is_active'), table_name='api_keys')
    op.drop_index(op.f('ix_api_keys_application_id'), table_name='api_keys')
    op.drop_table('api_keys')
    op.drop_index(op.f('ix_applications_status'), table_name='applications')
    op.drop_index(op.f('ix_applications_slug'), table_name='applications')
    op.drop_table('applications')