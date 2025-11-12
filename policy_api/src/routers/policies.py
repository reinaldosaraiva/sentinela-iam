"""
Policy management router
"""

import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import logging

import database
import models.policy

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=List[models.policy.PolicyResponse])
async def list_policies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    """List all policies"""
    policies = db.query(models.policy.Policy).offset(skip).limit(limit).all()
    return policies


@router.get("/{policy_id}", response_model=models.policy.PolicyResponse)
async def get_policy(
    policy_id: int,
    db: Session = Depends(database.get_db)
):
    """Get a specific policy by ID"""
    policy = db.query(models.policy.Policy).filter(models.policy.Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found"
        )
    return policy


@router.post("/", response_model=models.policy.PolicyResponse, status_code=status.HTTP_201_CREATED)
async def create_policy(
    policy: models.policy.PolicyCreate,
    db: Session = Depends(database.get_db)
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