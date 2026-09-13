from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, UploadFile, File, Form, Request, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.licensing.deps import get_current_licensed_user
from app.user.models import User
from app.staff.service import get_current_pharmacy_id
from app.staff.permissions import Permissions
from app.audit.schemas import AuditLogResponse, DocumentResponse
from app.audit.service import AuditService

router = APIRouter(tags=["Audit & Compliance"])


@router.get("/audit-logs", response_model=List[AuditLogResponse])
def get_audit_logs(
    action_type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    entity_type: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user),
):
    pharmacy_id = get_current_pharmacy_id(current_user)

    return AuditService.get_logs(
        db=db,
        pharmacy_id=pharmacy_id,
        action_type=action_type,
        category=category,
        user_id=user_id,
        entity_type=entity_type,
        limit=limit,
        offset=offset,
    )


@router.get("/documents", response_model=List[DocumentResponse])
def list_documents(
    category: Optional[str] = Query(None),
    entity_id: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user),
):
    pharmacy_id = get_current_pharmacy_id(current_user)

    return AuditService.list_documents(
        db=db,
        pharmacy_id=pharmacy_id,
        category=category,
        entity_id=entity_id,
        limit=limit,
        offset=offset,
    )


@router.post(
    "/documents/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    file: UploadFile = File(...),
    category: str = Form(...),
    title: str = Form(...),
    entity_id: Optional[str] = Form(None),
    expiry_date: Optional[datetime] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user),
):
    pharmacy_id = get_current_pharmacy_id(current_user)

    return AuditService.upload_document(
        db=db,
        pharmacy_id=pharmacy_id,
        user_id=str(current_user.id),
        file=file,
        category=category,
        title=title,
        entity_id=entity_id,
        expiry_date=expiry_date,
    )


@router.get("/documents/{document_id}/download")
def get_document_download_url(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user),
):
    pharmacy_id = get_current_pharmacy_id(current_user)

    return AuditService.get_document_url(
        db=db,
        pharmacy_id=pharmacy_id,
        document_id=document_id,
    )
