from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.base import get_db
from app.supplier.models import Supplier
from app.supplier.schemas import SupplierCreate, SupplierUpdate, SupplierResponse

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(
    supplier_in: SupplierCreate,
    pharmacy_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    data = supplier_in.model_dump(exclude_unset=True)
    target_pharmacy_id = pharmacy_id or data.get("pharmacy_id") or "default-pharmacy-id"
    valid_data = {k: v for k, v in data.items() if hasattr(Supplier, k)}
    valid_data["pharmacy_id"] = target_pharmacy_id

    db_supplier = Supplier(**valid_data)
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)

    # Sync with Financial System if balance/purchase value exists
    try:
        import httpx
        balance = float(getattr(db_supplier, 'outstanding_balance', 0) or getattr(db_supplier, 'opening_balance', 0) or 0)
        if balance > 0:
            httpx.post(
                "http://127.0.0.1:8080/finance/api/webhooks/internal/supplier-sync",
                json={
                    "supplier_name": db_supplier.name,
                    "transaction_type": "purchase",
                    "total_amount": balance,
                    "remarks": f"Opening balance/purchase sync for {db_supplier.name}"
                },
                timeout=3.0
            )
    except Exception as e:
        print(f"Failed to send supplier sync webhook to financial system: {e}")

    return db_supplier

@router.get("/", response_model=List[SupplierResponse])
def get_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    suppliers = db.query(Supplier).offset(skip).limit(limit).all()
    return suppliers

@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(supplier_id: str, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(supplier_id: str, supplier_in: SupplierUpdate, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    update_data = supplier_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(supplier, field):
            setattr(supplier, field, value)
        
    db.commit()
    db.refresh(supplier)
    return supplier

@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: str, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    db.delete(supplier)
    db.commit()
    return None