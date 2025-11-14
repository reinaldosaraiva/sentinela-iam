"""
Policy management router for Cedar policies
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import logging

from database_pg import get_db
from models.policy import Policy, PolicyStatus
from models.user import User
from schemas.policy import (
    PolicyCreate, PolicyUpdate, PolicyResponse, PolicyListResponse,
    PolicyValidationRequest, PolicyValidationResponse
)
from dependencies import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/policies", tags=["policies"])


@router.get("/", response_model=PolicyListResponse)
async def list_policies(
    skip: int = Query(0, ge=0, description="Number of policies to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of policies to return"),
    status: Optional[PolicyStatus] = Query(None, description="Filter by policy status"),
    search: Optional[str] = Query(None, description="Search by name or description"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List policies with pagination and filters"""
    
    # Build query
    query = db.query(Policy)
    
    # Apply filters
    if status:
        query = query.filter(Policy.status == status)
    if search:
        query = query.filter(
            (Policy.name.ilike(f"%{search}%")) |
            (Policy.description.ilike(f"%{search}%"))
        )
    
    # Count total
    total = query.count()
    
    # Apply pagination
    policies = query.offset(skip).limit(limit).all()
    
    return PolicyListResponse(
        policies=policies,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{policy_id}", response_model=PolicyResponse)
async def get_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get policy by ID"""
    
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    return policy


@router.post("/", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
async def create_policy(
    policy_data: PolicyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new policy"""
    try:
        # Create policy in database
        db_policy = models.policy.Policy(
            name=policy.name,
            description=policy.description,
            content=policy.content,
            version="1.0.0",
            status="draft",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(db_policy)
        db.commit()
        db.refresh(db_policy)
        
        # Notify OPAL about policy update
        # OPAL service will be integrated later
        logger.info(f"Policy {db_policy.id} created successfully")
        
        return db_policy
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating policy: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create policy"
        )


@router.put("/{policy_id}", response_model=models.policy.PolicyResponse)
async def update_policy(
    policy_id: int,
    policy_update: models.policy.PolicyUpdate,
    db: Session = Depends(database.get_db)
):
    """Update an existing policy"""
    try:
        db_policy = db.query(models.policy.Policy).filter(models.policy.Policy.id == policy_id).first()
        if not db_policy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Policy not found"
            )
        
        # Update policy fields
        update_data = policy_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_policy, field, value)
        
        db_policy.updated_at = datetime.utcnow()
        
        # Increment version if content changed
        if "content" in update_data:
            current_version = db_policy.version.split(".")
            current_version[-1] = str(int(current_version[-1]) + 1)
            db_policy.version = ".".join(current_version)
        
        db.commit()
        db.refresh(db_policy)
        
        # Notify OPAL about policy update
        # OPAL service will be integrated later
        logger.info(f"Policy {db_policy.id} updated successfully")
        
        return db_policy
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating policy: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update policy"
        )


@router.delete("/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy(
    policy_id: int,
    db: Session = Depends(database.get_db)
):
    """Delete a policy"""
    try:
        db_policy = db.query(models.policy.Policy).filter(models.policy.Policy.id == policy_id).first()
        if not db_policy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Policy not found"
            )
        
        # Store policy info for OPAL notification
        policy_info = {
            "id": db_policy.id,
            "name": db_policy.name
        }
        
        # Delete from database
        db.delete(db_policy)
        db.commit()
        
        # Notify OPAL about policy deletion
        # OPAL service will be integrated later
        logger.info(f"Policy {policy_id} deleted successfully")
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting policy: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete policy"
        )


@router.post("/{policy_id}/publish", response_model=models.policy.PolicyResponse)
async def publish_policy(
    policy_id: int,
    db: Session = Depends(database.get_db)
):
    """Publish a policy (make it active)"""
    try:
        db_policy = db.query(models.policy.Policy).filter(models.policy.Policy.id == policy_id).first()
        if not db_policy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Policy not found"
            )
        
        db_policy.status = "active"
        db_policy.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(db_policy)
        
        # Force OPAL notification
        # OPAL service will be integrated later
        logger.info(f"Policy {policy_id} published successfully")
        
        return db_policy
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error publishing policy: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to publish policy"
        )