"""
Application model for multi-application management
"""

from sqlalchemy import Column, String, Text, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

try:
    from ..database_pg import Base
except ImportError:
    from database_pg import Base


class Application(Base):
    """
    Application model representing an application registered in Sentinela

    Attributes:
        id: Unique identifier (UUID)
        name: Display name of the application
        slug: URL-friendly unique identifier
        description: Detailed description
        logo_url: URL to application logo
        website_url: Application website URL
        status: Application status (active, paused, archived)
        environment: Deployment environment (development, staging, production)
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
        created_by: UUID of user who created the application
        api_keys: Relationship to APIKey model
    """

    __tablename__ = "applications"

    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )

    # Basic Information
    name = Column(String(255), nullable=False)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)

    # URLs
    logo_url = Column(String(500), nullable=True)
    website_url = Column(String(500), nullable=True)

    # Status and Environment
    status = Column(
        String(20),
        nullable=False,
        default='active',
        index=True
    )
    environment = Column(
        String(20),
        nullable=False,
        default='development'
    )

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Creator
    created_by = Column(UUID(as_uuid=True), nullable=True)

    # Relationships
    api_keys = relationship("APIKey", back_populates="application", cascade="all, delete-orphan")
    resources = relationship("Resource", back_populates="application", cascade="all, delete-orphan")

    # Constraints
    __table_args__ = (
        CheckConstraint("status IN ('active', 'paused', 'archived')", name='check_application_status'),
        CheckConstraint("environment IN ('development', 'staging', 'production')", name='check_application_environment'),
    )

    def __repr__(self):
        return f"<Application(id={self.id}, name='{self.name}', slug='{self.slug}', status='{self.status}')>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': str(self.id),
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'logo_url': self.logo_url,
            'website_url': self.website_url,
            'status': self.status,
            'environment': self.environment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': str(self.created_by) if self.created_by else None,
            'api_keys_count': len(self.api_keys) if self.api_keys else 0
        }
