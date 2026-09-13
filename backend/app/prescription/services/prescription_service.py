import os
import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

from app.core.exceptions import NotFoundException
from app.core.storage import storage_service
from app.core.config import settings
from app.prescription.models import Prescription
from app.prescription.schemas import PrescriptionResponse, HumanReviewRequest
from app.audit.service import AuditService

class PrescriptionService:

    @staticmethod
    def upload_prescription(
        db: Session,
        pharmacy_id: str,
        user_id: str,
        user_email: str,
        file: UploadFile,
        branch_id: Optional[str] = None,
        customer_id: Optional[str] = None,
    ) -> PrescriptionResponse:
        ext = os.path.splitext(file.filename or "")[1]
        unique_key = f"{pharmacy_id}/prescriptions/{uuid.uuid4()}{ext}"
        bucket = settings.storage_bucket_prescriptions

        storage_service.upload_file(
            file_obj=file.file,
            bucket_name=bucket,
            object_name=unique_key,
            content_type=file.content_type or "image/jpeg",
        )

        prescription = Prescription(
            pharmacy_id=pharmacy_id,
            branch_id=branch_id,
            customer_id=customer_id,
            file_name=file.filename or "prescription_file",
            file_key=unique_key,
            status="UPLOADED",
        )
        db.add(prescription)
        db.flush()

        AuditService.log(
            db=db,
            pharmacy_id=pharmacy_id,
            user_id=user_id,
            user_email=user_email,
            action_type="PRESCRIPTION_UPLOAD",
            category="Prescription",
            entity_type="Prescription",
            entity_id=prescription.id,
            details={"file_name": prescription.file_name},
        )

        url = storage_service.get_presigned_url(bucket, unique_key)

        return PrescriptionResponse(
            id=prescription.id,
            pharmacy_id=prescription.pharmacy_id,
            branch_id=prescription.branch_id,
            customer_id=prescription.customer_id,
            file_name=prescription.file_name,
            extracted_text=prescription.extracted_text,
            analysis_result=prescription.analysis_result,
            status=prescription.status,
            reviewed_by_user_id=prescription.reviewed_by_user_id,
            reviewer_notes=prescription.reviewer_notes,
            created_at=prescription.created_at,
            download_url=url,
        )

    @staticmethod
    def get_prescription(db: Session, pharmacy_id: str, prescription_id: str) -> PrescriptionResponse:
        prescription = db.query(Prescription).filter(
            Prescription.id == prescription_id,
            Prescription.pharmacy_id == pharmacy_id
        ).first()
        if not prescription:
            raise NotFoundException("Prescription")

        bucket = settings.storage_bucket_prescriptions
        url = storage_service.get_presigned_url(bucket, prescription.file_key)

        return PrescriptionResponse(
            id=prescription.id,
            pharmacy_id=prescription.pharmacy_id,
            branch_id=prescription.branch_id,
            customer_id=prescription.customer_id,
            file_name=prescription.file_name,
            extracted_text=prescription.extracted_text,
            analysis_result=prescription.analysis_result,
            status=prescription.status,
            reviewed_by_user_id=prescription.reviewed_by_user_id,
            reviewer_notes=prescription.reviewer_notes,
            created_at=prescription.created_at,
            download_url=url,
        )

    @staticmethod
    def list_prescriptions(
        db: Session,
        pharmacy_id: str,
        status: Optional[str] = None,
        customer_id: Optional[str] = None,
    ) -> List[PrescriptionResponse]:
        q = db.query(Prescription).filter(Prescription.pharmacy_id == pharmacy_id)
        if status:
            q = q.filter(Prescription.status == status)
        if customer_id:
            q = q.filter(Prescription.customer_id == customer_id)

        prescriptions = q.order_by(Prescription.created_at.desc()).all()
        bucket = settings.storage_bucket_prescriptions

        results = []
        for p in prescriptions:
            url = storage_service.get_presigned_url(bucket, p.file_key)
            results.append(
                PrescriptionResponse(
                    id=p.id,
                    pharmacy_id=p.pharmacy_id,
                    branch_id=p.branch_id,
                    customer_id=p.customer_id,
                    file_name=p.file_name,
                    extracted_text=p.extracted_text,
                    analysis_result=p.analysis_result,
                    status=p.status,
                    reviewed_by_user_id=p.reviewed_by_user_id,
                    reviewer_notes=p.reviewer_notes,
                    created_at=p.created_at,
                    download_url=url,
                )
            )
        return results

    @staticmethod
    def submit_human_review(
        db: Session,
        pharmacy_id: str,
        user_id: str,
        user_email: str,
        prescription_id: str,
        data: HumanReviewRequest,
    ) -> PrescriptionResponse:
        prescription = db.query(Prescription).filter(
            Prescription.id == prescription_id,
            Prescription.pharmacy_id == pharmacy_id
        ).first()
        if not prescription:
            raise NotFoundException("Prescription")

        prescription.status = "REVIEWED" if data.approved else "REJECTED"
        prescription.reviewed_by_user_id = user_id
        prescription.reviewer_notes = data.reviewer_notes
        if data.corrected_result:
            prescription.analysis_result = data.corrected_result

        db.flush()

        AuditService.log(
            db=db,
            pharmacy_id=pharmacy_id,
            user_id=user_id,
            user_email=user_email,
            action_type="PRESCRIPTION_REVIEW",
            category="Prescription",
            entity_type="Prescription",
            entity_id=prescription.id,
            details={
                "approved": data.approved,
                "notes": data.reviewer_notes,
            }
        )

        bucket = settings.storage_bucket_prescriptions
        url = storage_service.get_presigned_url(bucket, prescription.file_key)

        return PrescriptionResponse(
            id=prescription.id,
            pharmacy_id=prescription.pharmacy_id,
            branch_id=prescription.branch_id,
            customer_id=prescription.customer_id,
            file_name=prescription.file_name,
            extracted_text=prescription.extracted_text,
            analysis_result=prescription.analysis_result,
            status=prescription.status,
            reviewed_by_user_id=prescription.reviewed_by_user_id,
            reviewer_notes=prescription.reviewer_notes,
            created_at=prescription.created_at,
            download_url=url,
        )
