"""
Policy schemas for API serialization
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import enum


class PolicyStatus(str, enum.Enum):
    """Policy status enumeration"""
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class PolicyBase(BaseModel):
    """Base policy schema"""
    name: str = Field(..., min_length=1, max_length=255, description="Policy name")
    description: Optional[str] = Field(None, description="Policy description")
    content: str = Field(..., description="Cedar policy content")


class PolicyCreate(PolicyBase):
    """Schema for creating a policy"""
    pass


class PolicyUpdate(BaseModel):
    """Schema for updating a policy"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Policy name")
    description: Optional[str] = Field(None, description="Policy description")
    content: Optional[str] = Field(None, description="Cedar policy content")
    status: Optional[PolicyStatus] = Field(None, description="Policy status")


class PolicyResponse(PolicyBase):
    """Schema for policy response"""
    id: int = Field(..., description="Policy ID")
    version: str = Field(..., description="Policy version")
    status: PolicyStatus = Field(..., description="Policy status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        from_attributes = True


class PolicyListResponse(BaseModel):
    """Schema for paginated policy list"""
    policies: List[PolicyResponse] = Field(..., description="List of policies")
    total: int = Field(..., description="Total number of policies")
    skip: int = Field(..., description="Number of policies skipped")
    limit: int = Field(..., description="Maximum number of policies returned")


class PolicyValidationRequest(BaseModel):
    """Policy validation request model"""
    content: str = Field(..., description="Cedar policy content to validate")


class PolicyValidationResponse(BaseModel):
    """Policy validation response model"""
    valid: bool = Field(..., description="Whether policy is valid")
    errors: List[str] = Field(default_factory=list, description="Validation errors")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")