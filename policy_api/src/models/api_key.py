"""
APIKey model for application authentication
"""

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import hashlib
import secrets

try:
    from ..database_pg import Base
except ImportError:
    from database_pg import Base


class APIKey(Base):
    """
    APIKey model for application authentication

    Attributes:
        id: Unique identifier (UUID)
        application_id: Foreign key to Application
        name: Friendly name for the API key
        key_prefix: Visible prefix (e.g., 'app_')
        key_hash: Hashed key for secure storage
        last_used_at: Timestamp of last usage
        expires_at: Optional expiration timestamp
        is_active: Whether the key is active
        created_at: Timestamp of creation
        application: Relationship to Application model
    """

    __tablename__ = "api_keys"

    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )

    # Foreign Key
    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey('applications.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    # Key Information
    name = Column(String(100), nullable=False)
    key_prefix = Column(String(10), nullable=False, default='app_')
    key_hash = Column(String(255), nullable=False)

    # Usage Tracking
    last_used_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    # Status
    is_active = Column(Boolean, nullable=False, default=True, index=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    application = relationship("Application", back_populates="api_keys")

    def __repr__(self):
        return f"<APIKey(id={self.id}, name='{self.name}', application_id={self.application_id}, active={self.is_active})>"

    @staticmethod
    def generate_key(prefix: str = "app_") -> tuple[str, str]:
        """
        Generate a new API key with prefix and hash

        Args:
            prefix: Key prefix (default: 'app_')

        Returns:
            Tuple of (plain_key, key_hash)
        """
        # Generate 32 bytes of random data (256 bits)
        random_bytes = secrets.token_bytes(32)
        # Encode as hex string
        random_string = random_bytes.hex()
        # Create full key
        plain_key = f"{prefix}{random_string}"
        # Hash the key for storage
        key_hash = hashlib.sha256(plain_key.encode()).hexdigest()

        return plain_key, key_hash

    @staticmethod
    def verify_key(plain_key: str, key_hash: str) -> bool:
        """
        Verify a plain key against its hash

        Args:
            plain_key: The plain text API key
            key_hash: The stored hash

        Returns:
            True if key matches hash, False otherwise
        """
        computed_hash = hashlib.sha256(plain_key.encode()).hexdigest()
        return computed_hash == key_hash

    def update_last_used(self):
        """Update the last_used_at timestamp"""
        self.last_used_at = datetime.utcnow()

    def is_expired(self) -> bool:
        """Check if the API key is expired"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at

    def is_valid(self) -> bool:
        """Check if the API key is valid (active and not expired)"""
        return self.is_active and not self.is_expired()

    def to_dict(self, include_hash: bool = False):
        """
        Convert model to dictionary

        Args:
            include_hash: Whether to include the key_hash (default: False)

        Returns:
            Dictionary representation
        """
        data = {
            'id': str(self.id),
            'application_id': str(self.application_id),
            'name': self.name,
            'key_prefix': self.key_prefix,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_active': self.is_active,
            'is_expired': self.is_expired(),
            'is_valid': self.is_valid(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        if include_hash:
            data['key_hash'] = self.key_hash

        return data
