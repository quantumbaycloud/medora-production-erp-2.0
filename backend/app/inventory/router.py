from fastapi import APIRouter, Depends, Query, UploadFile, File, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.base import get_db
from app.licensing.deps import get_current_licensed_user
from app.user.models import User
from app.staff.service import get_current_pharmacy_id
from app.staff.permissions import Permissions
from app.inventory.schemas import (
    InventoryLedgerResponse,
    StockAdjustmentCreate,
    ImportSummaryResponse,
)
from app.inventory.service import InventoryService
from app.inventory.services.export_service import ExportService
from app.inventory.services.import_service import ImportService

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/ledger", response_model=List[InventoryLedgerResponse])
def get_inventory_ledger(
    medicine_id: Optional[str] = Query(None),
    batch_number: Optional[str] = Query(None),
    transaction_type: Optional[str] = Query(None),
    branch_id: Optional[str] = Query(None),
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.INVENTORY_MANAGE.code)
    return InventoryService.get_ledger(
        db,
        pharmacy_id=active_pharmacy_id,
        medicine_id=medicine_id,
        batch_number=batch_number,
        transaction_type=transaction_type,
        branch_id=branch_id,
    )

@router.post("/adjust", response_model=InventoryLedgerResponse, status_code=status.HTTP_201_CREATED)
def adjust_stock(
    data: StockAdjustmentCreate,
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    branch_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.INVENTORY_AUDIT.code)
    return InventoryService.adjust_stock(db, active_pharmacy_id, current_user.id, data, branch_id)

@router.get("/export/{entity}")
def export_entity_data(
    entity: str,
    format: str = Query("csv", enum=["csv", "excel", "pdf"]),
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.REPORTS_EXPORT.code)
    df = ExportService.get_dataframe(db, active_pharmacy_id, entity)

    if format == "csv":
        buf = ExportService.export_csv(df)
        return StreamingResponse(
            buf,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=export_{entity}.csv"}
        )
    elif format == "excel":
        buf = ExportService.export_excel(df)
        return StreamingResponse(
            buf,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=export_{entity}.xlsx"}
        )
    elif format == "pdf":
        buf = ExportService.export_pdf(df, title=f"MEDORAX REPORT: {entity.upper()}")
        return StreamingResponse(
            buf,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=report_{entity}.pdf"}
        )

@router.post("/import/medicines", response_model=ImportSummaryResponse)
def import_medicines_csv(
    file: UploadFile = File(...),
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.INVENTORY_MANAGE.code)
    return ImportService.import_medicines_csv(db, active_pharmacy_id, file)
