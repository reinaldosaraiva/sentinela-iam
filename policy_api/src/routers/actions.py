"""
REST API endpoints for Action management
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

try:
    from ..database_pg import get_db
    from ..models import Action, Resource
    from ..schemas import (
        ActionCreate,
        ActionUpdate,
        ActionResponse,
        ActionListResponse
    )
    from ..dependencies import get_current_user
except ImportError:
    from database_pg import get_db
    from models import Action, Resource
    from schemas import (
        ActionCreate,
        ActionUpdate,
        ActionResponse,
        ActionListResponse
    )
    from dependencies import get_current_user

router = APIRouter(prefix="/actions", tags=["actions"])


# ============================================================================
# ACTION ENDPOINTS
# ============================================================================

@router.post("/", response_model=ActionResponse, status_code=status.HTTP_201_CREATED)
def create_action(
    action: ActionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new action

    - **action_type**: Unique identifier for action type (e.g., "read", "write", "delete")
    - **name**: Display name of the action
    - **description**: Detailed description (optional)
    - **resource_id**: Resource this action belongs to
    - **is_active**: Whether the action is active (default: true)
    """
    # Check if resource exists
    resource = db.query(Resource).filter(Resource.id == action.resource_id).first()
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with ID {action.resource_id} not found"
        )

    # Check if action_type already exists for this resource
    existing = db.query(Action).filter(
        Action.action_type == action.action_type,
        Action.resource_id == action.resource_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Action with type '{action.action_type}' already exists for this resource"
        )

    # Create new action
    db_action = Action(**action.model_dump())
    db.add(db_action)
    db.commit()
    db.refresh(db_action)

    return db_action


@router.get("/", response_model=ActionListResponse)
def list_actions(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    resource_id: UUID = Query(None, description="Filter by resource ID"),
    is_active: bool = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    List all actions with pagination and filtering

    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 10, max: 100)
    - **resource_id**: Filter by resource ID (optional)
    - **is_active**: Filter by active status (optional)
    """
    query = db.query(Action)

    # Apply filters
    if resource_id:
        query = query.filter(Action.resource_id == resource_id)
    if is_active is not None:
        query = query.filter(Action.is_active == is_active)

    # Count total
    total = query.count()

    # Pagination
    offset = (page - 1) * page_size
    actions = query.offset(offset).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "actions": actions
    }


@router.get("/{action_id}", response_model=ActionResponse)
def get_action(
    action_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get action by ID

    Returns detailed information about a specific action
    """
    action = db.query(Action).filter(Action.id == action_id).first()
    if not action:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Action with ID {action_id} not found"
        )

    return action


@router.put("/{action_id}", response_model=ActionResponse)
def update_action(
    action_id: UUID,
    action_update: ActionUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update an action

    Only provided fields will be updated. All fields are optional.
    """
    action = db.query(Action).filter(Action.id == action_id).first()
    if not action:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Action with ID {action_id} not found"
        )

    # Check action_type uniqueness if updating action_type
    if action_update.action_type and action_update.action_type != action.action_type:
        existing = db.query(Action).filter(
            Action.action_type == action_update.action_type,
            Action.resource_id == action.resource_id,
            Action.id != action_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Action with type '{action_update.action_type}' already exists for this resource"
            )

    # Update fields
    update_data = action_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(action, field, value)

    db.commit()
    db.refresh(action)

    return action


@router.delete("/{action_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_action(
    action_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete an action
    """
    action = db.query(Action).filter(Action.id == action_id).first()
    if not action:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Action with ID {action_id} not found"
        )

    db.delete(action)
    db.commit()

    return None


@router.patch("/{action_id}/deactivate", response_model=ActionResponse)
def deactivate_action(
    action_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Deactivate an action (soft delete)
    """
    action = db.query(Action).filter(Action.id == action_id).first()
    if not action:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Action with ID {action_id} not found"
        )

    action.is_active = False
    db.commit()
    db.refresh(action)

    return action


@router.patch("/{action_id}/activate", response_model=ActionResponse)
def activate_action(
    action_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Activate an action
    """
    action = db.query(Action).filter(Action.id == action_id).first()
    if not action:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Action with ID {action_id} not found"
        )

    action.is_active = True
    db.commit()
    db.refresh(action)

    return action
