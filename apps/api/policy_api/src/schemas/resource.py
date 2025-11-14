"""
Pydantic schemas for Resource
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
# from uuid import UUID  # Temporarily commented for compatibility


class ResourceBase(BaseModel):
    """Base schema for Resource"""
    resource_type: str = Field(..., min_length=1, max_length=100, pattern="^[a-z0-9_-]+$", description="Resource type identifier")
    name: str = Field(..., min_length=1, max_length=255, description="Resource display name")
    description: Optional[str] = Field(None, description="Resource description")
    is_active: bool = Field(True, description="Whether the resource is active")


class ResourceCreate(ResourceBase):
    """Schema for creating a resource"""
    application_id: int = Field(..., description="Application ID this resource belongs to")  # Temporarily int


class ResourceUpdate(BaseModel):
    """Schema for updating a resource"""
    resource_type: Optional[str] = Field(None, min_length=1, max_length=100, pattern="^[a-z0-9_-]+$")
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ResourceResponse(ResourceBase):
    """Schema for resource response"""
    id: int  # Temporarily int instead of UUID
    application_id: int  # Temporarily int instead of UUID
    created_at: Optional[datetime] = None  # Simplified
    updated_at: Optional[datetime] = None  # Simplified
    created_by: Optional[str] = None  # Temporarily string instead of UUID
    actions_count: int = 0

    class Config:
        from_attributes = True


class ResourceListResponse(BaseModel):
    """Schema for list of resources"""
    total: int
    page: int
    page_size: int
    resources: list[ResourceResponse]
