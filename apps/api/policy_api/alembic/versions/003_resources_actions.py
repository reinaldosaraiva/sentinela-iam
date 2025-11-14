"""Add resources and actions with sample data

Revision ID: 003_resources_actions
Revises: 002_add_missing_columns_simple
Create Date: 2025-11-13 11:25:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003_resources_actions'
down_revision: Union[str, None] = '002_add_missing_columns_simple'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add missing columns to existing tables
    op.add_column('resources', sa.Column('created_by', sa.String(length=100), nullable=True))
    op.add_column('actions', sa.Column('created_by', sa.String(length=100), nullable=True))
    
    # Insert sample data for resources
    op.execute("""
        INSERT INTO resources (application_id, resource_type, name, description, is_active, created_at, updated_at, created_by)
        VALUES 
            (1, 'documents', 'Document Management', 'Manage documents and files', true, NOW(), NOW(), 'admin'),
            (1, 'users', 'User Management', 'Manage user accounts and profiles', true, NOW(), NOW(), 'admin'),
            (1, 'billing', 'Billing System', 'Access billing and payment information', true, NOW(), NOW(), 'admin'),
            (2, 'dashboard', 'Dashboard', 'Main application dashboard', true, NOW(), NOW(), 'admin'),
            (2, 'reports', 'Reports', 'Generate and view reports', true, NOW(), NOW(), 'admin')
    """)
    
    # Insert sample data for actions
    op.execute("""
        INSERT INTO actions (resource_id, action_type, name, description, is_active, created_at, updated_at, created_by)
        VALUES 
            -- Document actions (resource_id = 1)
            (1, 'read', 'Read Documents', 'View and download documents', true, NOW(), NOW(), 'admin'),
            (1, 'write', 'Create Documents', 'Create new documents', true, NOW(), NOW(), 'admin'),
            (1, 'update', 'Update Documents', 'Edit existing documents', true, NOW(), NOW(), 'admin'),
            (1, 'delete', 'Delete Documents', 'Remove documents', true, NOW(), NOW(), 'admin'),
            
            -- User management actions (resource_id = 2)
            (2, 'read', 'View Users', 'View user profiles and information', true, NOW(), NOW(), 'admin'),
            (2, 'create', 'Create Users', 'Create new user accounts', true, NOW(), NOW(), 'admin'),
            (2, 'update', 'Update Users', 'Edit user information', true, NOW(), NOW(), 'admin'),
            (2, 'delete', 'Delete Users', 'Remove user accounts', true, NOW(), NOW(), 'admin'),
            
            -- Billing actions (resource_id = 3)
            (3, 'read', 'View Billing', 'View billing information and invoices', true, NOW(), NOW(), 'admin'),
            (3, 'pay', 'Make Payments', 'Process payments', true, NOW(), NOW(), 'admin'),
            
            -- Dashboard actions (resource_id = 4)
            (4, 'view', 'View Dashboard', 'Access main dashboard', true, NOW(), NOW(), 'admin'),
            (4, 'configure', 'Configure Dashboard', 'Customize dashboard layout', true, NOW(), NOW(), 'admin'),
            
            -- Reports actions (resource_id = 5)
            (5, 'read', 'View Reports', 'View existing reports', true, NOW(), NOW(), 'admin'),
            (5, 'generate', 'Generate Reports', 'Create new reports', true, NOW(), NOW(), 'admin'),
            (5, 'export', 'Export Reports', 'Export reports in various formats', true, NOW(), NOW(), 'admin')
    """)


def downgrade() -> None:
    # Remove sample data
    op.execute("DELETE FROM actions WHERE created_by = 'admin'")
    op.execute("DELETE FROM resources WHERE created_by = 'admin'")
    
    # Remove added columns
    op.drop_column('actions', 'created_by')
    op.drop_column('resources', 'created_by')