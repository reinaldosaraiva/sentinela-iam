"""
Documents API Router for Business API
Provides endpoints for document management
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# Mock documents database
documents_db = []
document_id_counter = 1

# Schemas
class DocumentBase(BaseModel):
    title: str
    content: str
    category: str

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    owner: str
    created_at: datetime
    updated_at: datetime

class DocumentListResponse(BaseModel):
    documents: List[DocumentResponse]
    total: int

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.get("/", response_model=DocumentListResponse)
async def list_documents():
    """List all documents"""
    return DocumentListResponse(
        documents=documents_db,
        total=len(documents_db)
    )

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: int):
    """Get a specific document"""
    document = next((doc for doc in documents_db if doc["id"] == document_id), None)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return document

@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(document: DocumentCreate):
    """Create a new document"""
    global document_id_counter
    
    new_document = {
        "id": document_id_counter,
        "title": document.title,
        "content": document.content,
        "category": document.category,
        "owner": "current_user",  # Would get from auth context
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    documents_db.append(new_document)
    document_id_counter += 1
    
    return new_document

@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(document_id: int, document: DocumentCreate):
    """Update a document"""
    doc_index = next((i for i, doc in enumerate(documents_db) if doc["id"] == document_id), None)
    if doc_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    updated_document = {
        **documents_db[doc_index],
        "title": document.title,
        "content": document.content,
        "category": document.category,
        "updated_at": datetime.now()
    }
    
    documents_db[doc_index] = updated_document
    return updated_document

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: int):
    """Delete a document"""
    doc_index = next((i for i, doc in enumerate(documents_db) if doc["id"] == document_id), None)
    if doc_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    documents_db.pop(doc_index)