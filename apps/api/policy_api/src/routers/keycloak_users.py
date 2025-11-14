"""
Keycloak User Management Router
Exposes Keycloak user management via REST API
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import os
import logging

from services.keycloak_admin import KeycloakAdminService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/keycloak/users", tags=["keycloak-users"])


# ==================== SCHEMAS ====================

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    firstName: str
    lastName: str
    password: str
    enabled: bool = True
    emailVerified: bool = False
    temporaryPassword: bool = False


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    enabled: Optional[bool] = None


class PasswordReset(BaseModel):
    newPassword: str
    temporary: bool = False


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    firstName: str
    lastName: str
    enabled: bool
    emailVerified: bool
    createdTimestamp: Optional[int] = None


class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int
    page: int
    perPage: int


# ==================== DEPENDENCIES ====================

async def get_keycloak_admin() -> KeycloakAdminService:
    """Get Keycloak Admin Service instance"""
    server_url = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
    realm = os.getenv("KEYCLOAK_REALM", "sentinela")
    client_id = os.getenv("KEYCLOAK_CLIENT_ID", "sentinela-api")
    client_secret = os.getenv("KEYCLOAK_CLIENT_SECRET", "sentinela-secret")
    admin_username = os.getenv("KEYCLOAK_ADMIN_USERNAME", "admin")
    admin_password = os.getenv("KEYCLOAK_ADMIN_PASSWORD", "admin123")

    service = KeycloakAdminService(
        server_url=server_url,
        realm=realm,
        client_id=client_id,
        client_secret=client_secret,
        admin_username=admin_username,
        admin_password=admin_password
    )

    try:
        yield service
    finally:
        await service.close()


# ==================== ENDPOINTS ====================

@router.get("/", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    perPage: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by username, email, or name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    username: Optional[str] = Query(None, description="Filter by username"),
    enabled: Optional[bool] = Query(None, description="Filter by enabled status"),
    keycloak: KeycloakAdminService = Depends(get_keycloak_admin)
):
    """List users with pagination and filters"""
    try:
        # Calculate offset
        first = (page - 1) * perPage

        # Get users from Keycloak
        users_data = await keycloak.list_users(
            search=search,
            first=first,
            max=perPage,
            email=email,
            username=username,
            enabled=enabled
        )

        # Get total count
        total = await keycloak.get_user_count()

        # Convert to response model
        users = [
            UserResponse(
                id=user.get("id"),
                username=user.get("username"),
                email=user.get("email", ""),
                firstName=user.get("firstName", ""),
                lastName=user.get("lastName", ""),
                enabled=user.get("enabled", True),
                emailVerified=user.get("emailVerified", False),
                createdTimestamp=user.get("createdTimestamp")
            )
            for user in users_data
        ]

        return UserListResponse(
            users=users,
            total=total,
            page=page,
            perPage=perPage
        )

    except Exception as e:
        logger.error(f"Error listing users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list users: {str(e)}"
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    keycloak: KeycloakAdminService = Depends(get_keycloak_admin)
):
    """Get user by ID"""
    try:
        user_data = await keycloak.get_user(user_id)

        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return UserResponse(
            id=user_data.get("id"),
            username=user_data.get("username"),
            email=user_data.get("email", ""),
            firstName=user_data.get("firstName", ""),
            lastName=user_data.get("lastName", ""),
            enabled=user_data.get("enabled", True),
            emailVerified=user_data.get("emailVerified", False),
            createdTimestamp=user_data.get("createdTimestamp")
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user: {str(e)}"
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    keycloak: KeycloakAdminService = Depends(get_keycloak_admin)
):
    """Create a new user"""
    try:
        user_id = await keycloak.create_user(
            username=user_data.username,
            email=user_data.email,
            first_name=user_data.firstName,
            last_name=user_data.lastName,
            password=user_data.password,
            enabled=user_data.enabled,
            email_verified=user_data.emailVerified,
            temporary_password=user_data.temporaryPassword
        )

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user. Username or email may already exist."
            )

        return {
            "id": user_id,
            "message": "User created successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


@router.put("/{user_id}")
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    keycloak: KeycloakAdminService = Depends(get_keycloak_admin)
):
    """Update user information"""
    try:
        success = await keycloak.update_user(
            user_id=user_id,
            email=user_data.email,
            first_name=user_data.firstName,
            last_name=user_data.lastName,
            enabled=user_data.enabled
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or update failed"
            )

        return {"message": "User updated successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}"
        )


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    keycloak: KeycloakAdminService = Depends(get_keycloak_admin)
):
    """Delete a user"""
    try:
        success = await keycloak.delete_user(user_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or deletion failed"
            )

        return {"message": "User deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}"
        )


@router.post("/{user_id}/reset-password")
async def reset_password(
    user_id: str,
    password_data: PasswordReset,
    keycloak: KeycloakAdminService = Depends(get_keycloak_admin)
):
    """Reset user password"""
    try:
        success = await keycloak.reset_password(
            user_id=user_id,
            new_password=password_data.newPassword,
            temporary=password_data.temporary
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or password reset failed"
            )

        return {"message": "Password reset successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resetting password for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reset password: {str(e)}"
        )


@router.get("/{user_id}/groups")
async def get_user_groups(
    user_id: str,
    keycloak: KeycloakAdminService = Depends(get_keycloak_admin)
):
    """Get groups that user belongs to"""
    try:
        groups = await keycloak.get_user_groups(user_id)
        return {"groups": groups}

    except Exception as e:
        logger.error(f"Error getting groups for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user groups: {str(e)}"
        )


@router.get("/stats/summary")
async def get_user_stats(
    keycloak: KeycloakAdminService = Depends(get_keycloak_admin)
):
    """Get user statistics"""
    try:
        total_users = await keycloak.get_user_count()

        # Get all users to calculate stats (for small datasets)
        # In production, consider caching or separate API calls
        users = await keycloak.list_users(first=0, max=1000)

        active_users = sum(1 for u in users if u.get("enabled", False))
        inactive_users = total_users - active_users

        return {
            "totalUsers": total_users,
            "activeUsers": active_users,
            "inactiveUsers": inactive_users
        }

    except Exception as e:
        logger.error(f"Error getting user stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user stats: {str(e)}"
        )
