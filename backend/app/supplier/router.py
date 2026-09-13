from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.db.base import get_db
from app.licensing.deps import get_current_licensed_user
from app.user.models import User
from app.staff.service import get_current_pharmacy_id
from app.staff.permissions import Permissions
from app.supplier.schemas import SupplierCreate, SupplierUpdate, SupplierResponse
from app.supplier.service import SupplierService

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@router.post("", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(
    data: SupplierCreate,
    pharmacy_id: str | None = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.PURCHASE_CREATE.code)
    return SupplierService.create_supplier(db, active_pharmacy_id, data)

@router.get("", response_model=List[SupplierResponse])
def list_suppliers(
    q: str = Query(None, description="Search by name, contact person, phone, or GSTIN"),
    pharmacy_id: str | None = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.PURCHASE_CREATE.code)
    return SupplierService.list_suppliers(db, active_pharmacy_id, q)

@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(
    supplier_id: str,
    pharmacy_id: str | None = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.PURCHASE_CREATE.code)
    return SupplierService.get_supplier(db, active_pharmacy_id, supplier_id)

@router.patch("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: str,
    data: SupplierUpdate,
    pharmacy_id: str | None = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.PURCHASE_CREATE.code)
    return SupplierService.update_supplier(db, active_pharmacy_id, supplier_id, data)

@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(
    supplier_id: str,
    pharmacy_id: str | None = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.PURCHASE_CREATE.code)
    SupplierService.delete_supplier(db, active_pharmacy_id, supplier_id)
