"""
Keycloak Group Management Router
Exposes Keycloak group management via REST API
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
import logging

from services.keycloak_admin import KeycloakAdminService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/keycloak/groups", tags=["keycloak-groups"])


# ==================== SCHEMAS ====================

class GroupCreate(BaseModel):
    name: str
    path: Optional[str] = None
    attributes: Optional[Dict[str, List[str]]] = None


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    attributes: Optional[Dict[str, List[str]]] = None


class GroupResponse(BaseModel):
    id: str
    name: str
    path: str
    subGroups: Optional[List[Dict]] = []
    attributes: Optional[Dict] = {}


class GroupMembershipRequest(BaseModel):
    userId: str
    groupId: str


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

@router.get("/")
async def list_groups(
    page: int = Query(1, ge=1, description="Page number"),
    perPage: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by group name"),
    keycloak: KeycloakAdminService = Depends(get_keycloak_admin)
):
    """List groups with pagination and filters"""
    try:
        # Calculate offset
        first = (page - 1) * perPage

        # Get groups from Keycloak
        groups_data = await keycloak.list_groups(
            search=search,
            first=first,
            max=perPage
        )

        # Get total count
        total = await keycloak.get_group_count()

        # Convert to response model
        groups = [
            GroupResponse(
                id=group.get("id"),
                name=group.get("name"),
                path=group.get("path", f"/{group.get('name')}"),
                subGroups=group.get("subGroups", []),
                attributes=group.get("attributes", {})
            )
            for group in groups_data
        ]

        return {
            "groups": groups,
            "total": total,
            "page": page,
            "perPage": perPage
        }

    except Exception as e:
        logger.error(f"Error listing groups: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list groups: {str(e)}"
        )


@router.get("/{group_id}", response_model=GroupResponse)
async def get_group(
    group_id: str,
    keycloak: KeycloakAdminService = Depends(get_keycloak_admin)
):
    """Get group by ID"""
    try:
        group_data = await keycloak.get_group(group_id)

        if not group_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found"
            )

        return GroupResponse(
            id=group_data.get("id"),
            name=group_data.get("name"),
            path=group_data.get("path", f"/{group_data.get('name')}"),
            subGroups=group_data.get("subGroups", []),
            attributes=group_data.get("attributes", {})
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting group {group_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get group: {str(e)}"
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_group(
    group_data: GroupCreate,
    keycloak: KeycloakAdminService = Depends(get_keycloak_admin)
):
    """Create a new group"""
    try:
        group_id = await keycloak.create_group(
            name=group_data.name,
            path=group_data.path,
            attributes=group_data.attributes
        )

        if not group_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create group. Group name may already exist."
            )

        return {
            "id": group_id,
            "message": "Group created successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating group: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create group: {str(e)}"
        )


@router.put("/{group_id}")
async def update_group(
    group_id: str,
    group_data: GroupUpdate,
    keycloak: KeycloakAdminService = Depends(get_keycloak_admin)
):
    """Update group information"""
    try:
        success = await keycloak.update_group(
            group_id=group_id,
            name=group_data.name,
            attributes=group_data.attributes
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found or update failed"
            )

        return {"message": "Group updated successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating group {group_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update group: {str(e)}"
        )


@router.delete("/{group_id}")
async def delete_group(
    group_id: str,
    keycloak: KeycloakAdminService = Depends(get_keycloak_admin)
):
    """Delete a group"""
    try:
        success = await keycloak.delete_group(group_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found or deletion failed"
            )

        return {"message": "Group deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting group {group_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete group: {str(e)}"
        )


@router.get("/{group_id}/members")
async def get_group_members(
    group_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    perPage: int = Query(50, ge=1, le=100, description="Items per page"),
    keycloak: KeycloakAdminService = Depends(get_keycloak_admin)
):
    """Get members of a group"""
    try:
        # Calculate offset
        first = (page - 1) * perPage

        members = await keycloak.get_group_members(
            group_id=group_id,
            first=first,
            max=perPage
        )

        return {
            "members": members,
            "total": len(members),
            "page": page,
            "perPage": perPage
        }

    except Exception as e:
        logger.error(f"Error getting members for group {group_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get group members: {str(e)}"
        )


@router.post("/{group_id}/members/{user_id}")
async def add_user_to_group(
    group_id: str,
    user_id: str,
    keycloak: KeycloakAdminService = Depends(get_keycloak_admin)
):
    """Add user to a group"""
    try:
        success = await keycloak.add_user_to_group(user_id, group_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to add user to group"
            )

        return {"message": "User added to group successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding user {user_id} to group {group_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add user to group: {str(e)}"
        )


@router.delete("/{group_id}/members/{user_id}")
async def remove_user_from_group(
    group_id: str,
    user_id: str,
    keycloak: KeycloakAdminService = Depends(get_keycloak_admin)
):
    """Remove user from a group"""
    try:
        success = await keycloak.remove_user_from_group(user_id, group_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to remove user from group"
            )

        return {"message": "User removed from group successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing user {user_id} from group {group_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to remove user from group: {str(e)}"
        )


@router.get("/stats/summary")
async def get_group_stats(
    keycloak: KeycloakAdminService = Depends(get_keycloak_admin)
):
    """Get group statistics"""
    try:
        total_groups = await keycloak.get_group_count()

        return {
            "totalGroups": total_groups
        }

    except Exception as e:
        logger.error(f"Error getting group stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get group stats: {str(e)}"
        )
