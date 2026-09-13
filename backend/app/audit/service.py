import os
import uuid
from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

from app.core.exceptions import NotFoundException
from app.core.storage import storage_service
from app.core.config import settings
from app.audit.models import AuditLog, DocumentMetadata
from app.audit.schemas import DocumentResponse


class AuditService:

    @staticmethod
    def log(
        db: Session,
        pharmacy_id: str,
        action_type: str,
        user_id: Optional[str] = None,
        user_email: Optional[str] = None,
        category: Optional[str] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:

        entry = AuditLog(
            pharmacy_id=pharmacy_id,
            user_id=user_id,
            user_email=user_email,
            action_type=action_type,
            category=category,
            entity_type=entity_type,
            entity_id=entity_id,
            ip_address=ip_address,
            details=details or {},
        )

        db.add(entry)
        db.flush()

        return entry

    @staticmethod
    def get_logs(
        db: Session,
        pharmacy_id: str,
        action_type: Optional[str] = None,
        category: Optional[str] = None,
        user_id: Optional[str] = None,
        entity_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[AuditLog]:

        q = db.query(AuditLog).filter(
            AuditLog.pharmacy_id == pharmacy_id
        )

        if action_type:
            q = q.filter(
                AuditLog.action_type == action_type
            )

        if category:
            q = q.filter(
                AuditLog.category == category
            )

        if user_id:
            q = q.filter(
                AuditLog.user_id == user_id
            )

        if entity_type:
            q = q.filter(
                AuditLog.entity_type == entity_type
            )

        return (
            q
            .order_by(AuditLog.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    @staticmethod
    def upload_document(
        db: Session,
        pharmacy_id: str,
        user_id: str,
        user_email: str,
        title: str,
        category: str,
        file: UploadFile,
        entity_id: Optional[str] = None,
        expiry_date: Optional[datetime] = None,
        ip_address: Optional[str] = None,
    ) -> DocumentResponse:

        content = file.file.read()
        file_size = len(content)
        file.file.seek(0)

        ext = os.path.splitext(
            file.filename or ""
        )[1]

        unique_key = (
            f"{pharmacy_id}/documents/{uuid.uuid4()}{ext}"
        )

        bucket = settings.storage_bucket_documents

        storage_service.upload_file(
            file_obj=file.file,
            bucket_name=bucket,
            object_name=unique_key,
            content_type=file.content_type
            or "application/octet-stream",
        )

        doc = DocumentMetadata(
            pharmacy_id=pharmacy_id,
            category=category,
            title=title,
            file_name=file.filename or "uploaded_file",
            file_key=unique_key,
            mime_type=file.content_type
            or "application/octet-stream",
            file_size_bytes=file_size,
            entity_id=entity_id,
            expiry_date=expiry_date,
            uploaded_by_user_id=user_id,
        )

        db.add(doc)
        db.flush()

        AuditService.log(
            db=db,
            pharmacy_id=pharmacy_id,
            user_id=user_id,
            user_email=user_email,
            action_type="DOCUMENT_UPLOAD",
            category="Documents",
            entity_type="Document",
            entity_id=doc.id,
            ip_address=ip_address,
            details={
                "title": title,
                "category": category,
                "file_name": doc.file_name,
                "file_size_bytes": file_size,
            },
        )

        url = storage_service.get_presigned_url(
            bucket,
            unique_key,
        )

        return DocumentResponse(
            id=doc.id,
            pharmacy_id=doc.pharmacy_id,
            category=doc.category,
            title=doc.title,
            file_name=doc.file_name,
            mime_type=doc.mime_type,
            file_size_bytes=doc.file_size_bytes,
            entity_id=doc.entity_id,
            expiry_date=doc.expiry_date,
            uploaded_by_user_id=doc.uploaded_by_user_id,
            created_at=doc.created_at,
            download_url=url,
        )

    @staticmethod
    def list_documents(
        db: Session,
        pharmacy_id: str,
        category: Optional[str] = None,
        entity_id: Optional[str] = None,
    ) -> list[DocumentResponse]:

        q = db.query(DocumentMetadata).filter(
            DocumentMetadata.pharmacy_id == pharmacy_id
        )

        if category:
            q = q.filter(
                DocumentMetadata.category == category
            )

        if entity_id:
            q = q.filter(
                DocumentMetadata.entity_id == entity_id
            )

        docs = (
            q
            .order_by(DocumentMetadata.created_at.desc())
            .all()
        )

        bucket = settings.storage_bucket_documents

        results = []

        for doc in docs:
            url = storage_service.get_presigned_url(
                bucket,
                doc.file_key,
            )

            results.append(
                DocumentResponse(
                    id=doc.id,
                    pharmacy_id=doc.pharmacy_id,
                    category=doc.category,
                    title=doc.title,
                    file_name=doc.file_name,
                    mime_type=doc.mime_type,
                    file_size_bytes=doc.file_size_bytes,
                    entity_id=doc.entity_id,
                    expiry_date=doc.expiry_date,
                    uploaded_by_user_id=doc.uploaded_by_user_id,
                    created_at=doc.created_at,
                    download_url=url,
                )
            )

        return results

    @staticmethod
    def get_document_url(
        db: Session,
        pharmacy_id: str,
        document_id: str,
    ) -> str:

        doc = (
            db.query(DocumentMetadata)
            .filter(
                DocumentMetadata.id == document_id,
                DocumentMetadata.pharmacy_id == pharmacy_id,
            )
            .first()
        )

        if not doc:
            raise NotFoundException("Document")

        bucket = settings.storage_bucket_documents

        url = storage_service.get_presigned_url(
            bucket,
            doc.file_key,
        )

        if not url:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate document download URL",
            )

        return url
