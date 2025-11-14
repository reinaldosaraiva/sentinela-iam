"""
User schemas for API serialization and validation
"""

from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserStatus(str, Enum):
    """User status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"


class UserRole(str, Enum):
    """User role enumeration"""
    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr = Field(..., description="User email address")
    name: str = Field(..., min_length=1, max_length=255, description="Full name")
    photo_url: Optional[str] = Field(None, max_length=500, description="Profile photo URL")
    status: UserStatus = Field(UserStatus.ACTIVE, description="User status")
    role: UserRole = Field(UserRole.USER, description="User role")

    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()


class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=8, max_length=255, description="Password")
    created_by: Optional[int] = Field(None, description="ID of user who creates this user")

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserUpdate(BaseModel):
    """User update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Full name")
    photo_url: Optional[str] = Field(None, max_length=500, description="Profile photo URL")
    role: Optional[UserRole] = Field(None, description="User role")

    @validator('name')
    def validate_name(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Name cannot be empty')
        return v.strip() if v else v


class UserStatusUpdate(BaseModel):
    """User status update schema"""
    status: UserStatus = Field(..., description="New user status")


class PasswordReset(BaseModel):
    """Password reset schema"""
    new_password: str = Field(..., min_length=8, max_length=255, description="New password")

    @validator('new_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class PasswordChange(BaseModel):
    """Password change schema"""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=255, description="New password")

    @validator('new_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserResponse(UserBase):
    """User response schema"""
    id: int = Field(..., description="User ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    created_by: Optional[int] = Field(None, description="ID of user who created this user")

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """User list response schema"""
    users: List[UserResponse] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Number of users per page")
    total_pages: int = Field(..., description="Total number of pages")


class UserSummary(BaseModel):
    """User summary for nested responses"""
    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    name: str = Field(..., description="User name")
    status: UserStatus = Field(..., description="User status")
    role: UserRole = Field(..., description="User role")

    class Config:
        from_attributes = True


class PhotoUpload(BaseModel):
    """Photo upload response schema"""
    photo_url: str = Field(..., description="Uploaded photo URL")
    message: str = Field(..., description="Upload result message")