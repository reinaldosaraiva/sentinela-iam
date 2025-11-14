"""
Document Pydantic Schemas for Business API
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class DocumentBase(BaseModel):
    """Base document schema"""
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Document content")
    classification: str = Field(default="public", description="Document classification")
    owner: str = Field(..., description="Document owner")


class DocumentCreate(DocumentBase):
    """Document creation schema"""
    pass


class DocumentUpdate(BaseModel):
    """Document update schema"""
    title: Optional[str] = Field(None, description="Document title")
    content: Optional[str] = Field(None, description="Document content")
    classification: Optional[str] = Field(None, description="Document classification")


class DocumentResponse(DocumentBase):
    """Document response schema"""
    id: int = Field(..., description="Document ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """Document list response schema"""
    documents: List[DocumentResponse] = Field(..., description="List of documents")
    total: int = Field(..., description="Total number of documents")
    skip: int = Field(default=0, description="Number of documents skipped")
    limit: int = Field(default=100, description="Number of documents returned")