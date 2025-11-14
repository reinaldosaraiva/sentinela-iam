"""
Group schemas for API serialization
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class GroupBase(BaseModel):
    """Base group schema"""
    name: str = Field(..., min_length=1, max_length=255, description="Group name")
    description: Optional[str] = Field(None, max_length=1000, description="Group description")
    parent_id: Optional[int] = Field(None, description="Parent group ID for hierarchy")


class GroupCreate(GroupBase):
    """Schema for creating a group"""
    pass


class GroupUpdate(BaseModel):
    """Schema for updating a group"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Group name")
    description: Optional[str] = Field(None, max_length=1000, description="Group description")
    parent_id: Optional[int] = Field(None, description="Parent group ID for hierarchy")


class GroupResponse(GroupBase):
    """Schema for group response"""
    id: int = Field(..., description="Group ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    created_by: Optional[int] = Field(None, description="Creator user ID")
    
    class Config:
        from_attributes = True


class GroupHierarchy(GroupResponse):
    """Schema for group with hierarchy information"""
    parent_name: Optional[str] = Field(None, description="Parent group name")
    children_count: int = Field(0, description="Number of child groups")
    users_count: int = Field(0, description="Number of users in group")


class GroupListResponse(BaseModel):
    """Schema for paginated group list"""
    groups: List[GroupResponse] = Field(..., description="List of groups")
    total: int = Field(..., description="Total number of groups")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")


class GroupTree(BaseModel):
    """Schema for group tree structure"""
    id: int
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    children: List['GroupTree'] = []

    class Config:
        from_attributes = True


# Update forward reference for GroupTree
GroupTree.model_rebuild()