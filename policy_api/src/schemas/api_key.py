"""
Pydantic schemas for APIKey
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class APIKeyBase(BaseModel):
    """Base schema for APIKey"""
    name: str = Field(..., min_length=1, max_length=100, description="API Key name")
    expires_at: Optional[datetime] = Field(None, description="Expiration date")


class APIKeyCreate(APIKeyBase):
    """Schema for creating an API key"""
    application_id: UUID = Field(..., description="Application ID")


class APIKeyCreateResponse(BaseModel):
    """Schema for API key creation response - includes plain key"""
    id: UUID
    application_id: UUID
    name: str
    key_prefix: str
    plain_key: str = Field(..., description="Plain text API key - SAVE THIS, it won't be shown again!")
    expires_at: Optional[datetime] = None
    is_active: bool = True
    created_at: datetime

    class Config:
        from_attributes = True


class APIKeyResponse(BaseModel):
    """Schema for API key response - WITHOUT plain key"""
    id: UUID
    application_id: UUID
    name: str
    key_prefix: str
    last_used_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    is_active: bool
    is_expired: bool
    is_valid: bool
    created_at: datetime

    class Config:
        from_attributes = True


class APIKeyUpdate(BaseModel):
    """Schema for updating an API key"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None


class APIKeyListResponse(BaseModel):
    """Schema for list of API keys"""
    total: int
    api_keys: list[APIKeyResponse]
