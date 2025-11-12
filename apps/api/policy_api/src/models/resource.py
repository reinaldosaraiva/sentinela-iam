"""
Resource model for IAM resources
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


class Resource(Base):
    """
    Resource model representing a protected resource in the IAM system

    A resource represents something that can be accessed or protected by policies.
    Examples: "users", "documents", "api", "billing", "settings"

    Attributes:
        id: Unique identifier (UUID)
        application_id: Foreign key to Application
        resource_type: Unique identifier for the resource type (e.g., "users", "documents")
        name: Display name of the resource
        description: Detailed description
        is_active: Whether the resource is active
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
        created_by: UUID of user who created the resource
        actions: Relationship to Action model
        application: Relationship to Application model
    """

    __tablename__ = "resources"

    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )

    # Application Reference
    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey('applications.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    # Resource Information
    resource_type = Column(String(100), nullable=False, index=True)
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
    actions = relationship("Action", back_populates="resource", cascade="all, delete-orphan")
    application = relationship("Application", back_populates="resources")

    def __repr__(self):
        return f"<Resource(id={self.id}, type='{self.resource_type}', name='{self.name}')>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': str(self.id),
            'application_id': str(self.application_id),
            'resource_type': self.resource_type,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': str(self.created_by) if self.created_by else None,
            'actions_count': len(self.actions) if self.actions else 0
        }
