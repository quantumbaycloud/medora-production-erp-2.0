from fastapi import APIRouter, Depends, Query, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.base import get_db
from app.licensing.deps import get_current_licensed_user
from app.user.models import User
from app.staff.service import get_current_pharmacy_id
from app.staff.permissions import Permissions
from app.prescription.schemas import (
    PrescriptionResponse,
    DrugInteractionRequest,
    AllergyWarningRequest,
    GenericMedicineRequest,
    HumanReviewRequest,
)
from app.prescription.services.prescription_service import PrescriptionService
from app.prescription.services.clinical_safety_service import ClinicalSafetyService
from app.prescription.tasks import process_prescription_task

router = APIRouter(prefix="/prescriptions", tags=["Prescription & Clinical Safety"])

@router.post("/upload", response_model=PrescriptionResponse, status_code=status.HTTP_201_CREATED)
def upload_prescription(
    file: UploadFile = File(...),
    branch_id: Optional[str] = Form(None),
    customer_id: Optional[str] = Form(None),
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.PRESCRIPTION_UPLOAD.code)
    res = PrescriptionService.upload_prescription(
        db=db,
        pharmacy_id=active_pharmacy_id,
        user_id=current_user.id,
        user_email=current_user.email or "unknown",
        file=file,
        branch_id=branch_id,
        customer_id=customer_id,
    )
    process_prescription_task.apply_async(args=[res.id, active_pharmacy_id], countdown=2)
    return res

@router.get("", response_model=List[PrescriptionResponse])
def list_prescriptions(
    status: Optional[str] = Query(None),
    customer_id: Optional[str] = Query(None),
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.PRESCRIPTION_UPLOAD.code)
    return PrescriptionService.list_prescriptions(db, active_pharmacy_id, status=status, customer_id=customer_id)

@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription(
    prescription_id: str,
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.PRESCRIPTION_UPLOAD.code)
    return PrescriptionService.get_prescription(db, active_pharmacy_id, prescription_id)

@router.post("/{prescription_id}/human-review", response_model=PrescriptionResponse)
def submit_human_review(
    prescription_id: str,
    data: HumanReviewRequest,
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.PRESCRIPTION_PROCESS.code)
    return PrescriptionService.submit_human_review(
        db=db,
        pharmacy_id=active_pharmacy_id,
        user_id=current_user.id,
        user_email=current_user.email or "unknown",
        prescription_id=prescription_id,
        data=data,
    )


@router.get("/{prescription_id}/analysis", response_model=PrescriptionResponse)
def get_prescription_analysis(
    prescription_id: str,
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.PRESCRIPTION_UPLOAD.code)
    # The analysis result is already attached to the standard response model.
    # We can just reuse get_prescription since the analysis JSON is already stored there.
    return PrescriptionService.get_prescription(db, active_pharmacy_id, prescription_id)

# --- Clinical Safety Endpoints ---


@router.post("/drug-interactions")
def check_drug_interactions(
    request: DrugInteractionRequest,
    current_user: User = Depends(get_current_licensed_user)
):
    return ClinicalSafetyService.check_drug_interactions(request.medicines)

@router.post("/allergy-warning")
def check_allergy_warning(
    request: AllergyWarningRequest,
    current_user: User = Depends(get_current_licensed_user)
):
    return ClinicalSafetyService.check_allergies(request.medicines, request.allergies)

@router.post("/generic-suggestions")
def get_generic_suggestions(
    request: GenericMedicineRequest,
    current_user: User = Depends(get_current_licensed_user)
):
    return ClinicalSafetyService.get_generic_suggestions(request.medicines)
