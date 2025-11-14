"""
User model for IAM system
"""

from sqlalchemy import Column, String, DateTime, Boolean, Enum, Integer, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

try:
    from ..database_pg import Base
except ImportError:
    from database_pg import Base


class UserStatus(str, enum.Enum):
    """User status enumeration"""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BLOCKED = "BLOCKED"


class UserRole(str, enum.Enum):
    """User role enumeration"""
    ADMIN = "ADMIN"
    USER = "USER"
    VIEWER = "VIEWER"


class User(Base):
    """
    User model representing IAM system users
    
    Attributes:
        id: Unique identifier (Integer for compatibility)
        email: Unique email address
        name: Full name of user
        password_hash: Hashed password
        photo_url: Profile photo URL
        status: User status (active/inactive/blocked)
        role: User role (admin/user/viewer)
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
        last_login: Last login timestamp
        created_by: User who created this user
    """

    __tablename__ = "users"

    # Primary Key
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )

    # User Information
    email = Column(
        String(255), 
        nullable=False, 
        unique=True, 
        index=True
    )
    name = Column(
        String(255), 
        nullable=False
    )
    password_hash = Column(
        String(255), 
        nullable=False
    )
    photo_url = Column(
        String(500), 
        nullable=True
    )

    # Status and Role
    status = Column(
        Enum(UserStatus), 
        nullable=False, 
        default=UserStatus.ACTIVE,
        index=True
    )
    role = Column(
        Enum(UserRole), 
        nullable=False, 
        default=UserRole.USER,
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
    last_login = Column(
        DateTime, 
        nullable=True
    )

    # Creator
    created_by = Column(
        Integer, 
        nullable=True
    )

    # Relationships
    # groups will be defined through UserGroup association table

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', status='{self.status}')>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'photo_url': self.photo_url,
            'status': self.status.value if self.status else None,
            'role': self.role.value if self.role else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_by': self.created_by
        }

    @property
    def is_active(self):
        """Check if user is active"""
        return self.status == UserStatus.ACTIVE

    @property
    def is_admin(self):
        """Check if user is admin"""
        return self.role == UserRole.ADMIN

    @property
    def display_name(self):
        """Get display name"""
        return self.name or self.email