"""
User-Group association schemas for API serialization
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class UserGroupBase(BaseModel):
    """Base user-group association schema"""
    user_id: int = Field(..., description="User ID")
    group_id: int = Field(..., description="Group ID")
    role_in_group: Optional[int] = Field(None, description="Role within group")
    is_active: bool = Field(True, description="Whether association is active")


class UserGroupCreate(UserGroupBase):
    """Schema for creating user-group association"""
    pass


class UserGroupUpdate(BaseModel):
    """Schema for updating user-group association"""
    role_in_group: Optional[int] = Field(None, description="Role within group")
    is_active: Optional[bool] = Field(None, description="Whether association is active")


class UserGroupResponse(UserGroupBase):
    """Schema for user-group association response"""
    added_at: datetime = Field(..., description="When user was added to group")
    added_by: Optional[int] = Field(None, description="Who added the user to group")
    
    class Config:
        from_attributes = True


class UserGroupListResponse(BaseModel):
    """Schema for paginated user-group list"""
    user_groups: List[UserGroupResponse] = Field(..., description="List of user-group associations")
    total: int = Field(..., description="Total number of associations")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")


class GroupMembershipResponse(BaseModel):
    """Schema for group membership information"""
    group_id: int
    group_name: str
    user_id: int
    user_email: str
    user_name: str
    role_in_group: Optional[int] = None
    is_active: bool
    added_at: datetime
    added_by: Optional[int] = None
    
    class Config:
        from_attributes = True


class UserMembershipResponse(BaseModel):
    """Schema for user membership information"""
    user_id: int
    user_email: str
    user_name: str
    group_id: int
    group_name: str
    role_in_group: Optional[int] = None
    is_active: bool
    added_at: datetime
    added_by: Optional[int] = None
    
    class Config:
        from_attributes = True


class BulkUserGroupOperation(BaseModel):
    """Schema for bulk user-group operations"""
    user_ids: List[int] = Field(..., description="List of user IDs")
    group_id: int = Field(..., description="Group ID")
    role_in_group: Optional[int] = Field(None, description="Role within group")