"""
Policy models for database and API
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import enum

try:
    from ..database_pg import Base
except ImportError:
    from database_pg import Base


class PolicyStatus(str, enum.Enum):
    """Policy status enumeration"""
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


# SQLAlchemy Model
class Policy(Base):
    """Policy database model"""
    __tablename__ = "policies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    version = Column(String(50), nullable=False, default="1.0.0")
    status = Column(Enum(PolicyStatus), nullable=False, default=PolicyStatus.DRAFT)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Policy(id={self.id}, name='{self.name}', status='{self.status}')>"


# Pydantic Models for API
class PolicyBase(BaseModel):
    """Base policy model"""
    name: str = Field(..., min_length=1, max_length=255, description="Policy name")
    description: Optional[str] = Field(None, description="Policy description")
    content: str = Field(..., description="Cedar policy content")


class PolicyCreate(PolicyBase):
    """Policy creation model"""
    pass


class PolicyUpdate(BaseModel):
    """Policy update model"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    content: Optional[str] = None
    status: Optional[PolicyStatus] = None


class PolicyResponse(PolicyBase):
    """Policy response model"""
    id: int
    version: str
    status: PolicyStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PolicyListResponse(BaseModel):
    """Policy list response model"""
    policies: list[PolicyResponse]
    total: int
    skip: int
    limit: int


class PolicyValidationRequest(BaseModel):
    """Policy validation request model"""
    content: str = Field(..., description="Cedar policy content to validate")


class PolicyValidationResponse(BaseModel):
    """Policy validation response model"""
    valid: bool
    errors: list[str] = []
    warnings: list[str] = []