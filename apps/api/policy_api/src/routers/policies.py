"""
Policy router for Cedar policy management
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


@router.post("/", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
async def create_policy(
    policy_data: PolicyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new Cedar policy"""
    
    # Only admins can create policies
    if current_user.role.value != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create policies"
        )
    
    # Check if policy name already exists
    existing_policy = db.query(Policy).filter(Policy.name == policy_data.name).first()
    if existing_policy:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Policy name already exists"
        )
    
    # Create policy
    db_policy = Policy(
        name=policy_data.name,
        description=policy_data.description,
        content=policy_data.content,
        version="1.0.0",
        status=PolicyStatus.DRAFT
    )
    
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    
    logger.info(f"Policy {db_policy.id} created successfully")
    return db_policy


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


@router.put("/{policy_id}", response_model=PolicyResponse)
async def update_policy(
    policy_id: int,
    policy_data: PolicyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing policy"""
    
    # Only admins can update policies
    if current_user.role.value != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update policies"
        )
    
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    # Check if new name conflicts with existing policies
    if policy_data.name and policy_data.name != policy.name:
        existing_policy = db.query(Policy).filter(Policy.name == policy_data.name).first()
        if existing_policy:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Policy name already exists"
            )
    
    # Update fields
    update_data = policy_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(policy, field, value)
    
    # Increment version if content changed
    if policy_data.content:
        current_version = policy.version.split(".")
        current_version[-1] = str(int(current_version[-1]) + 1)
        policy.version = ".".join(current_version)
    
    policy.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(policy)
    
    logger.info(f"Policy {policy_id} updated successfully")
    return policy


@router.delete("/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a policy"""
    
    # Only admins can delete policies
    if current_user.role.value != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete policies"
        )
    
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    # Don't allow deletion of active policies
    if policy.status == PolicyStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete active policy. Deactivate it first."
        )
    
    db.delete(policy)
    db.commit()
    
    logger.info(f"Policy {policy_id} deleted successfully")


@router.post("/{policy_id}/publish", response_model=PolicyResponse)
async def publish_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Publish a policy (make it active)"""
    
    # Only admins can publish policies
    if current_user.role.value != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can publish policies"
        )
    
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    policy.status = PolicyStatus.ACTIVE
    policy.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(policy)
    
    logger.info(f"Policy {policy_id} published successfully")
    return policy


@router.post("/{policy_id}/deactivate", response_model=PolicyResponse)
async def deactivate_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deactivate a policy"""
    
    # Only admins can deactivate policies
    if current_user.role.value != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can deactivate policies"
        )
    
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    policy.status = PolicyStatus.INACTIVE
    policy.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(policy)
    
    logger.info(f"Policy {policy_id} deactivated successfully")
    return policy


@router.post("/validate", response_model=PolicyValidationResponse)
async def validate_policy(
    validation_request: PolicyValidationRequest,
    current_user: User = Depends(get_current_user)
):
    """Validate Cedar policy syntax"""
    
    # Basic Cedar policy validation (simplified)
    errors = []
    warnings = []
    
    content = validation_request.content.strip()
    
    # Check if content is empty
    if not content:
        errors.append("Policy content cannot be empty")
        return PolicyValidationResponse(valid=False, errors=errors, warnings=warnings)
    
    # Basic Cedar syntax checks
    if not content.startswith("policy"):
        errors.append("Policy must start with 'policy' keyword")
    
    if "permit" not in content and "forbid" not in content:
        warnings.append("Policy should contain at least one 'permit' or 'forbid' rule")
    
    if "principal" not in content:
        warnings.append("Policy should reference 'principal' for proper access control")
    
    if "action" not in content:
        warnings.append("Policy should reference 'action' for proper access control")
    
    if "resource" not in content:
        warnings.append("Policy should reference 'resource' for proper access control")
    
    # Check for balanced braces
    open_braces = content.count("{")
    close_braces = content.count("}")
    if open_braces != close_braces:
        errors.append(f"Unbalanced braces: {open_braces} open, {close_braces} close")
    
    # Check for semicolon at end of statements
    lines = content.split("\n")
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if line and not line.startswith("//") and not line.endswith("{"):
            if any(keyword in line for keyword in ["permit", "forbid", "when", "unless"]):
                warnings.append(f"Line {i}: Statement may be missing semicolon")
    
    valid = len(errors) == 0
    
    return PolicyValidationResponse(
        valid=valid,
        errors=errors,
        warnings=warnings
    )


@router.get("/{policy_id}/export")
async def export_policy(
    policy_id: int,
    format: str = Query("cedar", description="Export format: cedar, json"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export policy in specified format"""
    
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    
    if format.lower() == "json":
        return {
            "id": policy.id,
            "name": policy.name,
            "description": policy.description,
            "content": policy.content,
            "version": policy.version,
            "status": policy.status.value,
            "created_at": policy.created_at.isoformat() if policy.created_at else None,
            "updated_at": policy.updated_at.isoformat() if policy.updated_at else None
        }
    else:
        # Default to Cedar format
        return policy.content