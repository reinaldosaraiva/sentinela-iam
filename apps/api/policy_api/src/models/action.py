"""
Action model for IAM actions
"""

from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

try:
    from ..database_pg import Base
except ImportError:
    from database_pg import Base


class Action(Base):
    """
    Action model representing an action that can be performed on a resource

    An action represents an operation that can be performed on a resource.
    Examples: "read", "write", "delete", "manage", "execute"

    Attributes:
        id: Unique identifier (UUID)
        resource_id: Foreign key to Resource
        action_type: Unique identifier for the action type (e.g., "read", "write")
        name: Display name of the action
        description: Detailed description
        is_active: Whether the action is active
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
        created_by: UUID of user who created the action
        resource: Relationship to Resource model
    """

    __tablename__ = "actions"

    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )

    # Resource Reference
    resource_id = Column(
        UUID(as_uuid=True),
        ForeignKey('resources.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    # Action Information
    action_type = Column(String(100), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Status
    is_active = Column(Boolean, nullable=False, default=True, index=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Creator
    created_by = Column(UUID(as_uuid=True), nullable=True)

    # Relationships
    resource = relationship("Resource", back_populates="actions")

    def __repr__(self):
        return f"<Action(id={self.id}, type='{self.action_type}', name='{self.name}')>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': str(self.id),
            'resource_id': str(self.resource_id),
            'action_type': self.action_type,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': str(self.created_by) if self.created_by else None
        }
