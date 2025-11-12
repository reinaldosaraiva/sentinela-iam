from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class DocumentType(str, Enum):
    CONTRACT = "contract"
    INVOICE = "invoice"
    REPORT = "report"
    MEMO = "memo"
    OTHER = "other"


class Document(BaseModel):
    id: str
    title: str
    content: str
    document_type: DocumentType
    owner_id: str
    department: str
    classification: str = "internal"
    created_at: datetime
    updated_at: datetime
    metadata: Optional[Dict[str, Any]] = None


class DocumentCreate(BaseModel):
    title: str
    content: str
    document_type: DocumentType
    department: str
    classification: str = "internal"
    metadata: Optional[Dict[str, Any]] = None


class DocumentResponse(BaseModel):
    id: str
    title: str
    content: str
    document_type: DocumentType
    owner_id: str
    department: str
    classification: str
    created_at: datetime
    updated_at: datetime
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True