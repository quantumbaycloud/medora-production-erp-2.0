from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class PrescriptionResponse(BaseModel):
    id: str
    pharmacy_id: str
    branch_id: Optional[str] = None
    customer_id: Optional[str] = None
    file_name: str
    extracted_text: Optional[str] = None
    analysis_result: Optional[Dict[str, Any]] = None
    status: str
    reviewed_by_user_id: Optional[str] = None
    reviewer_notes: Optional[str] = None
    created_at: Optional[datetime] = None
    download_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class DrugInteractionRequest(BaseModel):
    medicines: List[str]

class AllergyWarningRequest(BaseModel):
    medicines: List[str]
    allergies: List[str]

class GenericMedicineRequest(BaseModel):
    medicines: List[str]

class HumanReviewRequest(BaseModel):
    approved: bool
    reviewer_notes: Optional[str] = None
    corrected_result: Optional[Dict[str, Any]] = None
