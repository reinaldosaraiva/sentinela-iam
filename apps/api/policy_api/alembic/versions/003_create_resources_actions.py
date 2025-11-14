"""Create resources and actions tables with sample data

Revision ID: 003_create_resources_actions
Revises: 002_add_missing_columns_simple
Create Date: 2025-11-13 11:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003_create_resources_actions'
down_revision: Union[str, None] = '002_add_missing_columns_simple'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create resources table
    op.create_table('resources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('application_id', sa.Integer(), nullable=False),
        sa.Column('resource_type', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(['application_id'], ['applications.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resources_application_id'), 'resources', ['application_id'], unique=False)
    op.create_index(op.f('ix_resources_is_active'), 'resources', ['is_active'], unique=False)
    op.create_index(op.f('ix_resources_resource_type'), 'resources', ['resource_type'], unique=False)

    # Create actions table
    op.create_table('actions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('resource_id', sa.Integer(), nullable=False),
        sa.Column('action_type', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(['resource_id'], ['resources.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_actions_action_type'), 'actions', ['action_type'], unique=False)
    op.create_index(op.f('ix_actions_is_active'), 'actions', ['is_active'], unique=False)
    op.create_index(op.f('ix_actions_resource_id'), 'actions', ['resource_id'], unique=False)

    # Insert sample data
    op.execute("""
        INSERT INTO resources (id, application_id, resource_type, name, description, is_active, created_at, updated_at, created_by)
        VALUES 
            (1, 1, 'documents', 'Document Management', 'Manage documents and files', true, NOW(), NOW(), 'admin'),
            (2, 1, 'users', 'User Management', 'Manage user accounts and profiles', true, NOW(), NOW(), 'admin'),
            (3, 1, 'billing', 'Billing System', 'Access billing and payment information', true, NOW(), NOW(), 'admin'),
            (4, 2, 'dashboard', 'Dashboard', 'Main application dashboard', true, NOW(), NOW(), 'admin'),
            (5, 2, 'reports', 'Reports', 'Generate and view reports', true, NOW(), NOW(), 'admin')
    """)

    op.execute("""
        INSERT INTO actions (id, resource_id, action_type, name, description, is_active, created_at, updated_at, created_by)
        VALUES 
            -- Document actions
            (1, 1, 'read', 'Read Documents', 'View and download documents', true, NOW(), NOW(), 'admin'),
            (2, 1, 'write', 'Create Documents', 'Create new documents', true, NOW(), NOW(), 'admin'),
            (3, 1, 'update', 'Update Documents', 'Edit existing documents', true, NOW(), NOW(), 'admin'),
            (4, 1, 'delete', 'Delete Documents', 'Remove documents', true, NOW(), NOW(), 'admin'),
            
            -- User management actions
            (5, 2, 'read', 'View Users', 'View user profiles and information', true, NOW(), NOW(), 'admin'),
            (6, 2, 'create', 'Create Users', 'Create new user accounts', true, NOW(), NOW(), 'admin'),
            (7, 2, 'update', 'Update Users', 'Edit user information', true, NOW(), NOW(), 'admin'),
            (8, 2, 'delete', 'Delete Users', 'Remove user accounts', true, NOW(), NOW(), 'admin'),
            
            -- Billing actions
            (9, 3, 'read', 'View Billing', 'View billing information and invoices', true, NOW(), NOW(), 'admin'),
            (10, 3, 'pay', 'Make Payments', 'Process payments', true, NOW(), NOW(), 'admin'),
            
            -- Dashboard actions
            (11, 4, 'view', 'View Dashboard', 'Access main dashboard', true, NOW(), NOW(), 'admin'),
            (12, 4, 'configure', 'Configure Dashboard', 'Customize dashboard layout', true, NOW(), NOW(), 'admin'),
            
            -- Reports actions
            (13, 5, 'read', 'View Reports', 'View existing reports', true, NOW(), NOW(), 'admin'),
            (14, 5, 'generate', 'Generate Reports', 'Create new reports', true, NOW(), NOW(), 'admin'),
            (15, 5, 'export', 'Export Reports', 'Export reports in various formats', true, NOW(), NOW(), 'admin')
    """)


def downgrade() -> None:
    # Drop tables (reverse order due to foreign keys)
    op.drop_index(op.f('ix_actions_resource_id'), table_name='actions')
    op.drop_index(op.f('ix_actions_is_active'), table_name='actions')
    op.drop_index(op.f('ix_actions_action_type'), table_name='actions')
    op.drop_table('actions')
    
    op.drop_index(op.f('ix_resources_resource_type'), table_name='resources')
    op.drop_index(op.f('ix_resources_is_active'), table_name='resources')
    op.drop_index(op.f('ix_resources_application_id'), table_name='resources')
    op.drop_table('resources')