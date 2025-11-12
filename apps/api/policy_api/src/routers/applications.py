"""
REST API endpoints for Application management
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

try:
    from ..database_pg import get_db
    from ..models import Application, APIKey
    from ..schemas import (
        ApplicationCreate,
        ApplicationUpdate,
        ApplicationResponse,
        ApplicationListResponse,
        APIKeyCreate,
        APIKeyCreateResponse,
        APIKeyResponse,
        APIKeyListResponse
    )
    from ..dependencies import get_current_user
except ImportError:
    from database_pg import get_db
    from models import Application, APIKey
    from schemas import (
        ApplicationCreate,
        ApplicationUpdate,
        ApplicationResponse,
        ApplicationListResponse,
        APIKeyCreate,
        APIKeyCreateResponse,
        APIKeyResponse,
        APIKeyListResponse
    )
    from dependencies import get_current_user

router = APIRouter(prefix="/applications", tags=["applications"])


# ============================================================================
# APPLICATION ENDPOINTS
# ============================================================================

@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new application

    - **name**: Application name
    - **slug**: URL-friendly unique identifier
    - **description**: Detailed description (optional)
    - **status**: active, paused, or archived (default: active)
    - **environment**: development, staging, or production (default: development)
    """
    # Check if slug already exists
    existing = db.query(Application).filter(Application.slug == application.slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Application with slug '{application.slug}' already exists"
        )

    # Create new application
    db_application = Application(**application.model_dump())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)

    return db_application


@router.get("/", response_model=ApplicationListResponse)
def list_applications(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    status: str = Query(None, pattern="^(active|paused|archived)$", description="Filter by status"),
    environment: str = Query(None, pattern="^(development|staging|production)$", description="Filter by environment"),
    db: Session = Depends(get_db)
):
    """
    List all applications with pagination and filtering

    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 10, max: 100)
    - **status**: Filter by status (optional)
    - **environment**: Filter by environment (optional)
    """
    query = db.query(Application)

    # Apply filters
    if status:
        query = query.filter(Application.status == status)
    if environment:
        query = query.filter(Application.environment == environment)

    # Count total
    total = query.count()

    # Pagination
    offset = (page - 1) * page_size
    applications = query.offset(offset).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "applications": applications
    }


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get application by ID

    Returns detailed information about a specific application including API keys count
    """
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found"
        )

    return application


@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: UUID,
    application_update: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update an application

    Only provided fields will be updated. All fields are optional.
    """
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found"
        )

    # Check slug uniqueness if updating slug
    if application_update.slug and application_update.slug != application.slug:
        existing = db.query(Application).filter(Application.slug == application_update.slug).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Application with slug '{application_update.slug}' already exists"
            )

    # Update fields
    update_data = application_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)

    return application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete an application

    This will also delete all associated API keys (CASCADE).
    """
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found"
        )

    db.delete(application)
    db.commit()

    return None


# ============================================================================
# API KEY ENDPOINTS
# ============================================================================

@router.post("/{application_id}/api-keys", response_model=APIKeyCreateResponse, status_code=status.HTTP_201_CREATED)
def create_api_key(
    application_id: UUID,
    api_key_data: APIKeyCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new API key for an application

    **IMPORTANT**: The plain key is returned ONLY ONCE. Save it securely!

    - **name**: Friendly name for the API key
    - **expires_at**: Optional expiration date
    """
    # Verify application exists
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found"
        )

    # Generate API key
    plain_key, key_hash = APIKey.generate_key(prefix="app_")

    # Create API key record
    db_api_key = APIKey(
        application_id=application_id,
        name=api_key_data.name,
        key_prefix="app_",
        key_hash=key_hash,
        expires_at=api_key_data.expires_at
    )
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)

    # Return with plain key
    return APIKeyCreateResponse(
        id=db_api_key.id,
        application_id=db_api_key.application_id,
        name=db_api_key.name,
        key_prefix=db_api_key.key_prefix,
        plain_key=plain_key,  # ONLY shown once!
        expires_at=db_api_key.expires_at,
        is_active=db_api_key.is_active,
        created_at=db_api_key.created_at
    )


@router.get("/{application_id}/api-keys", response_model=APIKeyListResponse)
def list_api_keys(
    application_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    List all API keys for an application

    Returns all API keys with their status but WITHOUT the plain key.
    """
    # Verify application exists
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found"
        )

    api_keys = db.query(APIKey).filter(APIKey.application_id == application_id).all()

    return {
        "total": len(api_keys),
        "api_keys": [key.to_dict() for key in api_keys]
    }


@router.delete("/{application_id}/api-keys/{api_key_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_api_key(
    application_id: UUID,
    api_key_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete an API key
    """
    api_key = db.query(APIKey).filter(
        APIKey.id == api_key_id,
        APIKey.application_id == application_id
    ).first()

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"API Key with ID {api_key_id} not found for application {application_id}"
        )

    db.delete(api_key)
    db.commit()

    return None


@router.patch("/{application_id}/api-keys/{api_key_id}/deactivate", response_model=APIKeyResponse)
def deactivate_api_key(
    application_id: UUID,
    api_key_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Deactivate an API key (soft delete)
    """
    api_key = db.query(APIKey).filter(
        APIKey.id == api_key_id,
        APIKey.application_id == application_id
    ).first()

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"API Key with ID {api_key_id} not found for application {application_id}"
        )

    api_key.is_active = False
    db.commit()
    db.refresh(api_key)

    return api_key.to_dict()
