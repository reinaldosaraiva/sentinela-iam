"""
Pydantic schemas for Application
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime
# from uuid import UUID  # Temporarily commented for compatibility


class ApplicationBase(BaseModel):
    """Base schema for Application"""
    name: str = Field(..., min_length=1, max_length=255, description="Application name")
    slug: str = Field(..., min_length=1, max_length=100, pattern="^[a-z0-9-]+$", description="URL-friendly slug")
    description: Optional[str] = Field(None, description="Application description")
    logo_url: Optional[HttpUrl] = Field(None, description="Logo URL")
    website_url: Optional[HttpUrl] = Field(None, description="Website URL")
    status: str = Field("active", pattern="^(active|paused|archived)$", description="Application status")
    environment: str = Field("development", pattern="^(development|staging|production)$", description="Environment")


class ApplicationCreate(ApplicationBase):
    """Schema for creating an application"""
    pass


class ApplicationUpdate(BaseModel):
    """Schema for updating an application"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=100, pattern="^[a-z0-9-]+$")
    description: Optional[str] = None
    logo_url: Optional[HttpUrl] = None
    website_url: Optional[HttpUrl] = None
    status: Optional[str] = Field(None, pattern="^(active|paused|archived)$")
    environment: Optional[str] = Field(None, pattern="^(development|staging|production)$")


class ApplicationResponse(ApplicationBase):
    """Schema for application response"""
    id: int  # Temporarily int instead of UUID
    created_at: Optional[datetime] = None  # Simplified
    updated_at: Optional[datetime] = None  # Simplified
    created_by: Optional[str] = None  # Temporarily string instead of UUID
    api_keys_count: int = 0

    class Config:
        from_attributes = True


class ApplicationListResponse(BaseModel):
    """Schema for list of applications"""
    total: int
    page: int
    page_size: int
    applications: list[ApplicationResponse]
