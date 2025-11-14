"""Insert sample data for resources and actions

Revision ID: 004_sample_data
Revises: 003_resources_actions
Create Date: 2025-11-13 11:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '004_sample_data'
down_revision: Union[str, None] = '003_resources_actions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Insert sample data for resources
    op.execute("""
        INSERT INTO resources (application_id, resource_type, name, description, is_active, created_at, updated_at, created_by)
        SELECT * FROM (VALUES 
            (1, 'documents', 'Document Management', 'Manage documents and files', true, NOW(), NOW(), 'admin'),
            (1, 'users', 'User Management', 'Manage user accounts and profiles', true, NOW(), NOW(), 'admin'),
            (1, 'billing', 'Billing System', 'Access billing and payment information', true, NOW(), NOW(), 'admin'),
            (2, 'dashboard', 'Dashboard', 'Main application dashboard', true, NOW(), NOW(), 'admin'),
            (2, 'reports', 'Reports', 'Generate and view reports', true, NOW(), NOW(), 'admin')
        ) AS t(application_id, resource_type, name, description, is_active, created_at, updated_at, created_by)
        WHERE NOT EXISTS (
            SELECT 1 FROM resources WHERE resource_type = t.resource_type AND application_id = t.application_id
        )
    """)
    
    # Get the inserted resource IDs
    op.execute("""
        WITH resource_ids AS (
            SELECT id, resource_type FROM resources WHERE created_by = 'admin'
        )
        INSERT INTO actions (resource_id, action_type, name, description, is_active, created_at, updated_at, created_by)
        SELECT 
            r.id,
            a.action_type,
            a.name,
            a.description,
            a.is_active,
            NOW(),
            NOW(),
            'admin'
        FROM resource_ids r
        CROSS JOIN (VALUES 
            ('documents', 'read', 'Read Documents', 'View and download documents'),
            ('documents', 'write', 'Create Documents', 'Create new documents'),
            ('documents', 'update', 'Update Documents', 'Edit existing documents'),
            ('documents', 'delete', 'Delete Documents', 'Remove documents'),
            ('users', 'read', 'View Users', 'View user profiles and information'),
            ('users', 'create', 'Create Users', 'Create new user accounts'),
            ('users', 'update', 'Update Users', 'Edit user information'),
            ('users', 'delete', 'Delete Users', 'Remove user accounts'),
            ('billing', 'read', 'View Billing', 'View billing information and invoices'),
            ('billing', 'pay', 'Make Payments', 'Process payments'),
            ('dashboard', 'view', 'View Dashboard', 'Access main dashboard'),
            ('dashboard', 'configure', 'Configure Dashboard', 'Customize dashboard layout'),
            ('reports', 'read', 'View Reports', 'View existing reports'),
            ('reports', 'generate', 'Generate Reports', 'Create new reports'),
            ('reports', 'export', 'Export Reports', 'Export reports in various formats')
        ) AS a(resource_type, action_type, name, description, is_active)
        WHERE r.resource_type = a.resource_type
        AND NOT EXISTS (
            SELECT 1 FROM actions act 
            WHERE act.resource_id = r.id AND act.action_type = a.action_type
        )
    """)


def downgrade() -> None:
    # Remove sample data
    op.execute("DELETE FROM actions WHERE created_by = 'admin'")
    op.execute("DELETE FROM resources WHERE created_by = 'admin'")