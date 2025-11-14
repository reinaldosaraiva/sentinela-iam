"""
User-Group association model for many-to-many relationship
"""

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime

try:
    from ..database_pg import Base
except ImportError:
    from database_pg import Base


# Association table for User-Group many-to-many relationship
user_group_association = Table(
    'user_groups',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id', ondelete='CASCADE'), primary_key=True),
    Column('added_at', DateTime, nullable=False, default=datetime.utcnow),
    Column('added_by', Integer, ForeignKey('users.id'), nullable=True)
)


class UserGroup(Base):
    """
    User-Group association model for explicit many-to-many tracking
    
    This model provides additional metadata about user-group relationships
    beyond the basic association table.
    """

    __tablename__ = "user_group_metadata"

    # Composite Primary Key
    user_id = Column(
        Integer, 
        ForeignKey('users.id', ondelete='CASCADE'), 
        primary_key=True,
        nullable=False
    )
    group_id = Column(
        Integer, 
        ForeignKey('groups.id', ondelete='CASCADE'), 
        primary_key=True,
        nullable=False
    )

    # Metadata
    added_at = Column(
        DateTime, 
        nullable=False, 
        default=datetime.utcnow
    )
    added_by = Column(
        Integer, 
        ForeignKey('users.id'), 
        nullable=True
    )
    role_in_group = Column(
        Integer,  # Could be enum for member, admin, etc.
        nullable=True
    )
    is_active = Column(
        Integer,  # Using Integer for compatibility (0/1)
        nullable=False,
        default=1
    )

    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    group = relationship("Group", foreign_keys=[group_id])
    added_by_user = relationship("User", foreign_keys=[added_by])

    def __repr__(self):
        return f"<UserGroup(user_id={self.user_id}, group_id={self.group_id})>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'user_id': self.user_id,
            'group_id': self.group_id,
            'added_at': self.added_at.isoformat() if self.added_at else None,
            'added_by': self.added_by,
            'role_in_group': self.role_in_group,
            'is_active': bool(self.is_active) if self.is_active is not None else None
        }