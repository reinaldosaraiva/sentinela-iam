"""
Pydantic schemas for Action
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
# from uuid import UUID  # Temporarily commented for compatibility


class ActionBase(BaseModel):
    """Base schema for Action"""
    action_type: str = Field(..., min_length=1, max_length=100, pattern="^[a-z0-9_-]+$", description="Action type identifier")
    name: str = Field(..., min_length=1, max_length=255, description="Action display name")
    description: Optional[str] = Field(None, description="Action description")
    is_active: bool = Field(True, description="Whether the action is active")


class ActionCreate(ActionBase):
    """Schema for creating an action"""
    resource_id: int = Field(..., description="Resource ID this action belongs to")  # Temporarily int


class ActionUpdate(BaseModel):
    """Schema for updating an action"""
    action_type: Optional[str] = Field(None, min_length=1, max_length=100, pattern="^[a-z0-9_-]+$")
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ActionResponse(ActionBase):
    """Schema for action response"""
    id: int  # Temporarily int instead of UUID
    resource_id: int  # Temporarily int instead of UUID
    created_at: Optional[datetime] = None  # Simplified
    updated_at: Optional[datetime] = None  # Simplified
    created_by: Optional[str] = None  # Temporarily string instead of UUID

    class Config:
        from_attributes = True


class ActionListResponse(BaseModel):
    """Schema for list of actions"""
    total: int
    page: int
    page_size: int
    actions: list[ActionResponse]
