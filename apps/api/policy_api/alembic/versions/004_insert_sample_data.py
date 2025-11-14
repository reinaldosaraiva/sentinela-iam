"""Insert sample data for resources and actions

Revision ID: 004_insert_sample_data
Revises: 002_add_missing_columns_simple
Create Date: 2025-11-13 11:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '004_insert_sample_data'
down_revision: Union[str, None] = '002_add_missing_columns_simple'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Insert sample resources
    op.execute("""
        INSERT INTO resources (application_id, resource_type, name, description, is_active, created_at, updated_at, created_by)
        VALUES 
            (1, 'documents', 'Document Management', 'Manage documents and files', true, NOW(), NOW(), 'admin'),
            (2, 'users', 'User Management', 'Manage user accounts and profiles', true, NOW(), NOW(), 'admin'),
            (3, 'billing', 'Billing System', 'Access billing and payment information', true, NOW(), NOW(), 'admin'),
            (4, 'dashboard', 'Dashboard', 'Main application dashboard', true, NOW(), NOW(), 'admin'),
            (5, 'reports', 'Reports', 'Generate and view reports', true, NOW(), NOW(), 'admin')
        ON CONFLICT DO NOTHING
    """)

    # Insert sample actions
    op.execute("""
        INSERT INTO actions (resource_id, action_type, name, description, is_active, created_at, updated_at, created_by)
        VALUES 
            -- Document actions
            (1, 'read', 'Read Documents', 'View and download documents', true, NOW(), NOW(), 'admin'),
            (2, 'write', 'Create Documents', 'Create new documents', true, NOW(), NOW(), 'admin'),
            (3, 'update', 'Update Documents', 'Edit existing documents', true, NOW(), NOW(), 'admin'),
            (4, 'delete', 'Delete Documents', 'Remove documents', true, NOW(), NOW(), 'admin'),
            
            -- User management actions
            (5, 'read', 'View Users', 'View user profiles and information', true, NOW(), NOW(), 'admin'),
            (6, 'create', 'Create Users', 'Create new user accounts', true, NOW(), NOW(), 'admin'),
            (7, 'update', 'Update Users', 'Edit user information', true, NOW(), NOW(), 'admin'),
            (8, 'delete', 'Delete Users', 'Remove user accounts', true, NOW(), NOW(), 'admin'),
            
            -- Billing actions
            (9, 'read', 'View Billing', 'View billing information and invoices', true, NOW(), NOW(), 'admin'),
            (10, 'pay', 'Make Payments', 'Process payments', true, NOW(), NOW(), 'admin'),
            
            -- Dashboard actions
            (11, 'view', 'View Dashboard', 'Access main dashboard', true, NOW(), NOW(), 'admin'),
            (12, 'configure', 'Configure Dashboard', 'Customize dashboard layout', true, NOW(), NOW(), 'admin'),
            
            -- Reports actions
            (13, 'read', 'View Reports', 'View existing reports', true, NOW(), NOW(), 'admin'),
            (14, 'generate', 'Generate Reports', 'Create new reports', true, NOW(), NOW(), 'admin'),
            (15, 'export', 'Export Reports', 'Export reports in various formats', true, NOW(), NOW(), 'admin')
        ON CONFLICT DO NOTHING
    """)


def downgrade() -> None:
    # Remove sample data
    op.execute("DELETE FROM actions WHERE created_by = 'admin'")
    op.execute("DELETE FROM resources WHERE created_by = 'admin'")