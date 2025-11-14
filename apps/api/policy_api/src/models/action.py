"""
Action model for IAM actions
"""

from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
# import uuid  # Temporarily commented for compatibility

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
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )

    # Resource Reference
    resource_id = Column(
        Integer,
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
    created_by = Column(String(100), nullable=True)  # Temporarily string instead of UUID

    # Relationships
    resource = relationship("Resource", back_populates="actions")

    def __repr__(self):
        return f"<Action(id={self.id}, type='{self.action_type}', name='{self.name}')>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'resource_id': self.resource_id,
            'action_type': self.action_type,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': None,  # Simplified
            'updated_at': None,  # Simplified
            'created_by': self.created_by
        }
