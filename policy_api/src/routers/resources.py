"""
REST API endpoints for Resource management
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

try:
    from ..database_pg import get_db
    from ..models import Resource, Application
    from ..schemas import (
        ResourceCreate,
        ResourceUpdate,
        ResourceResponse,
        ResourceListResponse
    )
    from ..dependencies import get_current_user
except ImportError:
    from database_pg import get_db
    from models import Resource, Application
    from schemas import (
        ResourceCreate,
        ResourceUpdate,
        ResourceResponse,
        ResourceListResponse
    )
    from dependencies import get_current_user

router = APIRouter(prefix="/resources", tags=["resources"])


# ============================================================================
# RESOURCE ENDPOINTS
# ============================================================================

@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
def create_resource(
    resource: ResourceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new resource

    - **resource_type**: Unique identifier for resource type (e.g., "users", "documents")
    - **name**: Display name of the resource
    - **description**: Detailed description (optional)
    - **application_id**: Application this resource belongs to
    - **is_active**: Whether the resource is active (default: true)
    """
    # Check if application exists
    application = db.query(Application).filter(Application.id == resource.application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {resource.application_id} not found"
        )

    # Check if resource_type already exists for this application
    existing = db.query(Resource).filter(
        Resource.resource_type == resource.resource_type,
        Resource.application_id == resource.application_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Resource with type '{resource.resource_type}' already exists for this application"
        )

    # Create new resource
    db_resource = Resource(**resource.model_dump())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)

    return db_resource


@router.get("/", response_model=ResourceListResponse)
def list_resources(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    application_id: UUID = Query(None, description="Filter by application ID"),
    is_active: bool = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    List all resources with pagination and filtering

    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 10, max: 100)
    - **application_id**: Filter by application ID (optional)
    - **is_active**: Filter by active status (optional)
    """
    query = db.query(Resource)

    # Apply filters
    if application_id:
        query = query.filter(Resource.application_id == application_id)
    if is_active is not None:
        query = query.filter(Resource.is_active == is_active)

    # Count total
    total = query.count()

    # Pagination
    offset = (page - 1) * page_size
    resources = query.offset(offset).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "resources": resources
    }


@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(
    resource_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get resource by ID

    Returns detailed information about a specific resource including actions count
    """
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with ID {resource_id} not found"
        )

    return resource


@router.put("/{resource_id}", response_model=ResourceResponse)
def update_resource(
    resource_id: UUID,
    resource_update: ResourceUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update a resource

    Only provided fields will be updated. All fields are optional.
    """
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with ID {resource_id} not found"
        )

    # Check resource_type uniqueness if updating resource_type
    if resource_update.resource_type and resource_update.resource_type != resource.resource_type:
        existing = db.query(Resource).filter(
            Resource.resource_type == resource_update.resource_type,
            Resource.application_id == resource.application_id,
            Resource.id != resource_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Resource with type '{resource_update.resource_type}' already exists for this application"
            )

    # Update fields
    update_data = resource_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(resource, field, value)

    db.commit()
    db.refresh(resource)

    return resource


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(
    resource_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a resource

    This will also delete all associated actions (CASCADE).
    """
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with ID {resource_id} not found"
        )

    db.delete(resource)
    db.commit()

    return None


@router.patch("/{resource_id}/deactivate", response_model=ResourceResponse)
def deactivate_resource(
    resource_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Deactivate a resource (soft delete)
    """
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with ID {resource_id} not found"
        )

    resource.is_active = False
    db.commit()
    db.refresh(resource)

    return resource


@router.patch("/{resource_id}/activate", response_model=ResourceResponse)
def activate_resource(
    resource_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Activate a resource
    """
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with ID {resource_id} not found"
        )

    resource.is_active = True
    db.commit()
    db.refresh(resource)

    return resource
