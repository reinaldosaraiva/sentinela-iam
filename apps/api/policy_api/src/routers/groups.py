"""
Group router for IAM system
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database_pg import get_db
from models.group import Group
from models.user import User
from models.user_group import UserGroup
from schemas.group import (
    GroupCreate, GroupUpdate, GroupResponse, GroupListResponse,
    GroupHierarchy, GroupTree
)
from schemas.user_group import (
    UserGroupResponse, GroupMembershipResponse, UserMembershipResponse,
    BulkUserGroupOperation
)
from dependencies import get_current_user

router = APIRouter(prefix="/api/v1/groups", tags=["groups"])


@router.post("/", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(
    group_data: GroupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new group"""
    
    # Check if current user is admin
    if current_user.role.value != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create groups"
        )
    
    # Check if group name already exists
    existing_group = db.query(Group).filter(Group.name == group_data.name).first()
    if existing_group:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Group name already exists"
        )
    
    # Check if parent group exists (if specified)
    if group_data.parent_id:
        parent_group = db.query(Group).filter(Group.id == group_data.parent_id).first()
        if not parent_group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent group not found"
            )
    
    # Create group
    db_group = Group(
        name=group_data.name,
        description=group_data.description,
        parent_id=group_data.parent_id,
        created_by=current_user.id
    )
    
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    
    return db_group


@router.get("/", response_model=GroupListResponse)
async def list_groups(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    parent_id: Optional[int] = Query(None, description="Filter by parent group"),
    search: Optional[str] = Query(None, description="Search by name or description"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List groups with pagination and filters"""
    
    # Build query
    query = db.query(Group)
    
    # Apply filters
    if parent_id is not None:
        query = query.filter(Group.parent_id == parent_id)
    if search:
        query = query.filter(
            (Group.name.ilike(f"%{search}%")) |
            (Group.description.ilike(f"%{search}%"))
        )
    
    # Count total
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * per_page
    groups = query.offset(offset).limit(per_page).all()
    
    # Calculate total pages
    total_pages = (total + per_page - 1) // per_page
    
    return GroupListResponse(
        groups=groups,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )


@router.get("/{group_id}", response_model=GroupHierarchy)
async def get_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get group by ID with hierarchy information"""
    
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    # Get parent name
    parent_name = None
    if group.parent_id:
        parent = db.query(Group).filter(Group.id == group.parent_id).first()
        parent_name = parent.name if parent else None
    
    # Count children
    children_count = db.query(Group).filter(Group.parent_id == group_id).count()
    
    # Count users
    users_count = db.query(UserGroup).filter(UserGroup.group_id == group_id, UserGroup.is_active == 1).count()
    
    return GroupHierarchy(
        id=group.id,
        name=group.name,
        description=group.description,
        parent_id=group.parent_id,
        parent_name=parent_name,
        children_count=children_count,
        users_count=users_count,
        created_at=group.created_at,
        updated_at=group.updated_at,
        created_by=group.created_by
    )


@router.put("/{group_id}", response_model=GroupResponse)
async def update_group(
    group_id: int,
    group_data: GroupUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update group information"""
    
    # Only admins can update groups
    if current_user.role.value != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update groups"
        )
    
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    # Check if new name conflicts with existing groups
    if group_data.name and group_data.name != group.name:
        existing_group = db.query(Group).filter(Group.name == group_data.name).first()
        if existing_group:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Group name already exists"
            )
    
    # Check if parent group exists (if specified)
    if group_data.parent_id and group_data.parent_id != group.parent_id:
        # Prevent circular reference
        if group_data.parent_id == group_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Group cannot be its own parent"
            )
        
        parent_group = db.query(Group).filter(Group.id == group_data.parent_id).first()
        if not parent_group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent group not found"
            )
    
    # Update fields
    update_data = group_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(group, field, value)
    
    group.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(group)
    
    return group


@router.delete("/{group_id}")
async def delete_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete group (soft delete by checking dependencies)"""
    
    # Only admins can delete groups
    if current_user.role.value != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete groups"
        )
    
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    # Check if group has children
    children_count = db.query(Group).filter(Group.parent_id == group_id).count()
    if children_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete group with child groups. Delete children first."
        )
    
    # Check if group has users
    users_count = db.query(UserGroup).filter(UserGroup.group_id == group_id, UserGroup.is_active == 1).count()
    if users_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete group with users. Remove users first."
        )
    
    # Delete group
    db.delete(group)
    db.commit()
    
    return {"message": "Group deleted successfully"}


@router.get("/tree/hierarchy", response_model=List[GroupTree])
async def get_group_tree(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get complete group hierarchy as tree"""
    
    # Get all groups
    groups = db.query(Group).all()
    
    # Build tree structure (simple implementation)
    # In production, this would use recursive CTE for better performance
    group_dict = {group.id: GroupTree(id=group.id, name=group.name, description=group.description, parent_id=group.parent_id) for group in groups}
    
    # Build hierarchy
    root_groups = []
    for group in groups:
        group_tree = group_dict[group.id]
        if group.parent_id is None:
            root_groups.append(group_tree)
        else:
            parent = group_dict.get(group.parent_id)
            if parent:
                parent.children.append(group_tree)
    
    return root_groups


@router.post("/{group_id}/users/{user_id}", response_model=UserGroupResponse)
async def add_user_to_group(
    group_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add user to group"""
    
    # Only admins can manage group memberships
    if current_user.role.value != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can manage group memberships"
        )
    
    # Check if group exists
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if user is already in group
    existing_membership = db.query(UserGroup).filter(
        UserGroup.user_id == user_id,
        UserGroup.group_id == group_id
    ).first()
    
    if existing_membership:
        if existing_membership.is_active:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User is already a member of this group"
            )
        else:
            # Reactivate existing membership
            existing_membership.is_active = 1
            existing_membership.added_at = datetime.utcnow()
            existing_membership.added_by = current_user.id
            db.commit()
            db.refresh(existing_membership)
            return existing_membership
    
    # Create new user-group association
    user_group = UserGroup(
        user_id=user_id,
        group_id=group_id,
        added_by=current_user.id,
        is_active=1
    )
    
    db.add(user_group)
    db.commit()
    db.refresh(user_group)
    
    return user_group


@router.delete("/{group_id}/users/{user_id}")
async def remove_user_from_group(
    group_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove user from group"""
    
    # Only admins can manage group memberships
    if current_user.role.value != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can manage group memberships"
        )
    
    # Check if group exists
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if user is in group
    user_group = db.query(UserGroup).filter(
        UserGroup.user_id == user_id,
        UserGroup.group_id == group_id,
        UserGroup.is_active == 1
    ).first()
    
    if not user_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not a member of this group"
        )
    
    # Deactivate membership (soft delete)
    user_group.is_active = 0
    db.commit()
    
    return {"message": "User removed from group successfully"}


@router.get("/{group_id}/members", response_model=List[GroupMembershipResponse])
async def get_group_members(
    group_id: int,
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all users in a group"""
    
    # Check if group exists
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    # Get group members with user details
    query = db.query(UserGroup, User).join(
        User, UserGroup.user_id == User.id
    ).filter(
        UserGroup.group_id == group_id,
        UserGroup.is_active == 1
    )
    
    # Apply pagination
    offset = (page - 1) * per_page
    results = query.offset(offset).limit(per_page).all()
    
    members = []
    for user_group, user in results:
        members.append(GroupMembershipResponse(
            group_id=group_id,
            group_name=group.name,
            user_id=user.id,
            user_email=user.email,
            user_name=user.name,
            role_in_group=user_group.role_in_group,
            is_active=bool(user_group.is_active),
            added_at=user_group.added_at,
            added_by=user_group.added_by
        ))
    
    return members


@router.post("/{group_id}/members/bulk")
async def add_multiple_users_to_group(
    group_id: int,
    operation: BulkUserGroupOperation,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add multiple users to a group"""
    
    # Only admins can manage group memberships
    if current_user.role.value != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can manage group memberships"
        )
    
    # Check if group exists
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    # Verify operation is for the correct group
    if operation.group_id != group_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group ID in operation does not match URL parameter"
        )
    
    added_count = 0
    skipped_count = 0
    
    for user_id in operation.user_ids:
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            skipped_count += 1
            continue
        
        # Check if user is already in group
        existing_membership = db.query(UserGroup).filter(
            UserGroup.user_id == user_id,
            UserGroup.group_id == group_id
        ).first()
        
        if existing_membership:
            if existing_membership.is_active:
                skipped_count += 1
                continue
            else:
                # Reactivate existing membership
                existing_membership.is_active = 1
                existing_membership.added_at = datetime.utcnow()
                existing_membership.added_by = current_user.id
                if operation.role_in_group is not None:
                    existing_membership.role_in_group = operation.role_in_group
                added_count += 1
        else:
            # Create new user-group association
            user_group = UserGroup(
                user_id=user_id,
                group_id=group_id,
                role_in_group=operation.role_in_group,
                added_by=current_user.id,
                is_active=1
            )
            db.add(user_group)
            added_count += 1
    
    db.commit()
    
    return {
        "message": f"Bulk operation completed",
        "added_count": added_count,
        "skipped_count": skipped_count,
        "total_requested": len(operation.user_ids)
    }


@router.get("/users/{user_id}/groups", response_model=List[UserMembershipResponse])
async def get_user_groups(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all groups for a user"""
    
    # Users can view their own groups, admins can view any user's groups
    if current_user.role.value != 'admin' and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own group memberships"
        )
    
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get user's groups with group details
    query = db.query(UserGroup, Group).join(
        Group, UserGroup.group_id == Group.id
    ).filter(
        UserGroup.user_id == user_id,
        UserGroup.is_active == 1
    )
    
    results = query.all()
    
    memberships = []
    for user_group, group in results:
        memberships.append(UserMembershipResponse(
            user_id=user_id,
            user_email=user.email,
            user_name=user.name,
            group_id=group.id,
            group_name=group.name,
            role_in_group=user_group.role_in_group,
            is_active=bool(user_group.is_active),
            added_at=user_group.added_at,
            added_by=user_group.added_by
        ))
    
    return memberships