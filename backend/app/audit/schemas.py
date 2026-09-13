from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime


class AuditLogResponse(BaseModel):
    id: str
    pharmacy_id: str
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    action_type: str
    category: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    ip_address: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class DocumentResponse(BaseModel):
    id: str
    pharmacy_id: str
    category: str
    title: str
    file_name: str
    mime_type: str
    file_size_bytes: int
    entity_id: Optional[str] = None
    expiry_date: Optional[datetime] = None
    uploaded_by_user_id: Optional[str] = None
    created_at: Optional[datetime] = None
    download_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
