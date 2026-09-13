from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db  # Adjust import based on your real session utility file
from app.models.inventory import OpeningStock  # Adjust path to your model file

router = APIRouter()

@router.get("/opening-stock")
async def get_opening_stock(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    warehouse: Optional[str] = Query(None),
    pharmacy_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(OpeningStock)
    
    # 1. Apply multi-column query filtering parameters
    if pharmacy_id:
        query = query.filter(OpeningStock.pharmacy_id == pharmacy_id)
    if search:
        query = query.filter(
            OpeningStock.medicine_name.icontains(search) | OpeningStock.sku.icontains(search)
        )
    if category:
        query = query.filter(OpeningStock.category == category)
    if warehouse:
        query = query.filter(OpeningStock.location == warehouse)

    records = query.all()

    # 2. Compute aggregated metrics for dashboard summary panels
    total_items = len(records)
    total_qty = sum(item.opening_qty for item in records)
    # Simple calculation example: assuming baseline unit asset cost average valuation multiplier
    computed_value = total_qty * 12.50 
    
    # Format value into standard abbreviated short strings (e.g. $2.4M or $150.00)
    if computed_value >= 1_000_000:
        total_value = f"{computed_value / 1_000_000:.1f}M"
    else:
        total_value = f"{computed_value:,.2f}"

    return {
        "summary": {
            "totalItems": total_items,
            "totalValue": total_value,
            "startDate": "Oct 01, 2023"
        },
        "items": [
            {
                "id": r.id,
                "medicine_name": r.medicine_name,
                "sku": r.sku,
                "category": r.category,
                "opening_qty": r.opening_qty,
                "unit": r.unit,
                "location": r.location,
                "remarks": r.remarks,
                "period_start_date": r.period_start_date.strftime("%b %d, %Y") if r.period_start_date else "—"
            } for r in records
        ]
    }

@router.post("/opening-stock", status_code=status.HTTP_201_CREATED)
async def create_opening_stock(payload: dict, db: Session = Depends(get_db)):
    try:
        new_record = OpeningStock(
            pharmacy_id=payload.get("pharmacy_id", "default-pharmacy-id"), # Update based on your multitenant authentication layer
            medicine_name=payload.get("medicine_name"),
            sku=payload.get("sku"),
            category=payload.get("category"),
            opening_qty=payload.get("opening_qty", 0),
            unit=payload.get("unit", "Units"),
            location=payload.get("location"),
            remarks=payload.get("remarks")
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return {"status": "success", "id": new_record.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
