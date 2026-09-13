from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.db.base import get_db
from app.licensing.deps import get_current_licensed_user
from app.user.models import User
from app.staff.service import get_current_pharmacy_id
from app.staff.permissions import Permissions
from app.medicine.schemas import (
    MedicineCreate, MedicineUpdate, MedicineResponse,
    MedicineBatchCreate, MedicineBatchResponse
)
from app.medicine.service import MedicineService

router = APIRouter(prefix="/medicines", tags=["Medicines"])

@router.post("", response_model=MedicineResponse, status_code=status.HTTP_201_CREATED)
def create_medicine(
    data: MedicineCreate,
    pharmacy_id: str | None = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.MEDICINE_MANAGE.code)
    return MedicineService.create_medicine(db, active_pharmacy_id, data)

@router.get("", response_model=List[MedicineResponse])
def search_medicines(
    q: str = Query(None, description="Search by name, barcode, or SKU"),
    pharmacy_id: str | None = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.MEDICINE_READ.code)
    return MedicineService.search_medicines(db, active_pharmacy_id, q)

@router.get("/{medicine_id}", response_model=MedicineResponse)
def get_medicine(
    medicine_id: str,
    pharmacy_id: str | None = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.MEDICINE_READ.code)
    return MedicineService.get_medicine(db, active_pharmacy_id, medicine_id)

@router.patch("/{medicine_id}", response_model=MedicineResponse)
def update_medicine(
    medicine_id: str,
    data: MedicineUpdate,
    pharmacy_id: str | None = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.MEDICINE_MANAGE.code)
    return MedicineService.update_medicine(db, active_pharmacy_id, medicine_id, data)

@router.post("/{medicine_id}/batches", response_model=MedicineBatchResponse, status_code=status.HTTP_201_CREATED)
def add_medicine_batch(
    medicine_id: str,
    data: MedicineBatchCreate,
    pharmacy_id: str | None = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.INVENTORY_MANAGE.code)
    return MedicineService.add_batch(db, active_pharmacy_id, medicine_id, data)

@router.get("/{medicine_id}/batches", response_model=List[MedicineBatchResponse])
def get_medicine_batches(
    medicine_id: str,
    pharmacy_id: str | None = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.MEDICINE_READ.code)
    MedicineService.get_medicine(db, active_pharmacy_id, medicine_id)
    return MedicineService.list_medicine_batches(db, medicine_id)
