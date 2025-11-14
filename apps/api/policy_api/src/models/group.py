"""
Group model for IAM system
"""

from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

try:
    from ..database_pg import Base
except ImportError:
    from database_pg import Base


class Group(Base):
    """
    Group model representing organizational groups
    
    Attributes:
        id: Unique identifier (Integer for compatibility)
        name: Unique group name
        description: Group description
        parent_id: Parent group ID for hierarchy
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
        created_by: User who created this group
    """

    __tablename__ = "groups"

    # Primary Key
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )

    # Group Information
    name = Column(
        String(255), 
        nullable=False, 
        unique=True, 
        index=True
    )
    description = Column(
        Text, 
        nullable=True
    )

    # Hierarchy
    parent_id = Column(
        Integer, 
        ForeignKey('groups.id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )

    # Timestamps
    created_at = Column(
        DateTime, 
        nullable=False, 
        default=datetime.utcnow
    )
    updated_at = Column(
        DateTime, 
        nullable=False, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )

    # Creator
    created_by = Column(
        Integer, 
        nullable=True
    )

    # Relationships
    parent = relationship("Group", remote_side=[id], back_populates="children")
    children = relationship("Group", back_populates="parent", cascade="all, delete-orphan")
    # users will be defined through UserGroup association table

    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}', parent_id={self.parent_id})>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by
        }

    @property
    def is_root(self):
        """Check if group is root (no parent)"""
        return self.parent_id is None

    @property
    def hierarchy_path(self):
        """Get hierarchy path (placeholder - would need recursive query)"""
        # This would typically be implemented with a recursive CTE
        # For now, return simple representation
        return self.name