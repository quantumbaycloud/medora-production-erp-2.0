import json
import logging
import tempfile
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.core.celery_app import celery_app
from app.core.storage import storage_service
from app.core.config import settings
from app.prescription.models import Prescription
from app.prescription.services.ocr_service import OCRService
from app.prescription.services.ai_service import AIService
from app.prescription.services.verification_service import MedicineVerificationService
from app.prescription.services.clinical_safety_service import ClinicalSafetyService

logger = logging.getLogger(__name__)

@celery_app.task(name="process_prescription_task", bind=True, max_retries=3)
def process_prescription_task(self, prescription_id: str, pharmacy_id: str):
    db: Session = SessionLocal()
    try:
        prescription = db.query(Prescription).filter(
            Prescription.id == prescription_id,
            Prescription.pharmacy_id == pharmacy_id
        ).first()

        if not prescription:
            logger.error(f"Prescription {prescription_id} not found for pharmacy {pharmacy_id}")
            return {"success": False, "error": "Prescription not found"}

        if prescription.status != "UPLOADED":
            return {"success": False, "error": f"Prescription already in state {prescription.status}"}

        prescription.status = "PROCESSING"
        db.commit()

        bucket = settings.storage_bucket_prescriptions
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            local_path = tmp_file.name
            
        try:
            # Download file from S3 to local for OpenCV/PaddleOCR
            # S3 client wrapper download_file might not be directly in storage_service, let's use boto3 if needed.
            # Assuming storage_service.client exists
            storage_service.download_file(bucket, prescription.file_key, local_path)
            
            # 1. OCR Extraction
            text = OCRService.extract_text(local_path)
            if not text or not text.strip():
                prescription.status = "FAILED"
                db.commit()
                return {"success": False, "error": "OCR did not extract any text"}
            
            prescription.extracted_text = text
            db.commit()

            # 2. AI Extraction
            ai_result = AIService.analyze_prescription(text)
            if not ai_result or "error" in ai_result:
                prescription.status = "FAILED"
                db.commit()
                return {"success": False, "error": ai_result.get("error", "AI Analysis failed")}
            
            # 3. Medicine Verification
            medicines = ai_result.get("medicines", [])
            verification = MedicineVerificationService.verify_prescription(db, pharmacy_id, medicines)
            verified_medicines = verification.get("medicines", [])
            
            # Append verification details
            for idx, item in enumerate(verified_medicines):
                if idx < len(medicines):
                    medicines[idx]["confidence"] = item.get("confidence")
                    medicines[idx]["verificationStatus"] = item.get("status")
                    medicines[idx]["reviewStatus"] = item.get("reviewStatus")
                    medicines[idx]["matchedMedicine"] = item.get("matchedMedicine")
                    medicines[idx]["generic"] = item.get("generic")

            ai_result["medicines"] = medicines
            ai_result["overallReviewStatus"] = (
                "NEEDS_HUMAN_REVIEW"
                if any(item.get("reviewStatus") == "NEEDS_HUMAN_REVIEW" for item in verified_medicines)
                else "AUTO_VERIFIED"
            )

            # 4. Clinical Safety
            extracted_names = [m.get("matchedMedicine") or m.get("name") for m in medicines if m.get("name")]
            drug_interactions = ClinicalSafetyService.check_drug_interactions(extracted_names)
            
            ai_result["clinicalSafety"] = {
                "interactions": drug_interactions
            }

            # 5. Persist
            prescription.analysis_result = ai_result
            prescription.status = "REVIEWED" if ai_result["overallReviewStatus"] == "AUTO_VERIFIED" else "COMPLETED"
            db.commit()

            return {"success": True, "prescription_id": prescription_id}

        except Exception as e:
            logger.exception("Error processing prescription")
            prescription.status = "FAILED"
            db.commit()
            return {"success": False, "error": str(e)}

    except Exception as e:
        db.rollback()
        logger.exception("Database error in process_prescription_task")
        return {"success": False, "error": "Database error"}
    finally:
        db.close()
