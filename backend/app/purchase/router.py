from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.base import get_db
from app.licensing.deps import get_current_licensed_user
from app.user.models import User
from app.staff.service import get_current_pharmacy_id
from app.staff.permissions import Permissions
from app.purchase.schemas import (
    PurchaseInvoiceCreate,
    PurchaseInvoiceUpdate,
    PurchaseInvoiceResponse,
)
from app.purchase.service import PurchaseService

router = APIRouter(prefix="/purchases", tags=["Purchases"])

@router.post("", response_model=PurchaseInvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_purchase(
    data: PurchaseInvoiceCreate,
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.PURCHASE_CREATE.code)
    return PurchaseService.create_purchase(db, active_pharmacy_id, current_user.id, data)

@router.get("", response_model=List[PurchaseInvoiceResponse])
def list_purchases(
    supplier_id: Optional[str] = Query(None),
    branch_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.PURCHASE_CREATE.code)
    return PurchaseService.list_purchases(db, active_pharmacy_id, supplier_id, branch_id, status)

@router.get("/{purchase_id}", response_model=PurchaseInvoiceResponse)
def get_purchase(
    purchase_id: str,
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.PURCHASE_CREATE.code)
    return PurchaseService.get_purchase(db, active_pharmacy_id, purchase_id)

@router.patch("/{purchase_id}", response_model=PurchaseInvoiceResponse)
def update_purchase(
    purchase_id: str,
    data: PurchaseInvoiceUpdate,
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.PURCHASE_CREATE.code)
    return PurchaseService.update_purchase(db, active_pharmacy_id, purchase_id, data)

@router.post("/{purchase_id}/approve", response_model=PurchaseInvoiceResponse)
def approve_purchase(
    purchase_id: str,
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    # Segregation of duties: Requires PURCHASE_APPROVE permission
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.PURCHASE_APPROVE.code)
    return PurchaseService.approve_purchase(db, active_pharmacy_id, current_user.id, purchase_id)
