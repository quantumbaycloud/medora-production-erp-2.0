from datetime import date
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.base import get_db
from app.licensing.deps import get_current_licensed_user
from app.user.models import User
from app.staff.service import get_current_pharmacy_id
from app.staff.permissions import Permissions
from app.reports.schemas import (
    DashboardKPIResponse,
    SalesReportItem,
    ExpiryReportItem,
    GSTReportItem,
)
from app.reports.service import ReportService

router = APIRouter(prefix="/reports", tags=["Reports & Analytics"])

@router.get("/dashboard", response_model=DashboardKPIResponse)
def get_dashboard_kpis(
    branch_id: Optional[str] = Query(None),
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.REPORTS_READ.code)
    return ReportService.get_dashboard_kpis(db, active_pharmacy_id, branch_id)

@router.get("/sales")
def get_sales_report(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    branch_id: Optional[str] = Query(None),
    export: str = Query("json", enum=["json", "excel"]),
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    perm = Permissions.REPORTS_EXPORT.code if export == "excel" else Permissions.REPORTS_READ.code
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, perm)

    result = ReportService.generate_sales_report(
        db=db,
        pharmacy_id=active_pharmacy_id,
        start_date=start_date,
        end_date=end_date,
        branch_id=branch_id,
        export_excel=(export == "excel"),
    )

    if export == "excel":
        return StreamingResponse(
            result,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=sales_report.xlsx"}
        )
    return result

@router.get("/expiry")
def get_expiry_report(
    days_ahead: int = Query(60, ge=1, le=365),
    export: str = Query("json", enum=["json", "excel"]),
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    perm = Permissions.REPORTS_EXPORT.code if export == "excel" else Permissions.REPORTS_READ.code
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, perm)

    result = ReportService.generate_expiry_report(
        db=db,
        pharmacy_id=active_pharmacy_id,
        days_ahead=days_ahead,
        export_excel=(export == "excel"),
    )

    if export == "excel":
        return StreamingResponse(
            result,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=expiry_report.xlsx"}
        )
    return result

@router.get("/gst")
def get_gst_report(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    export: str = Query("json", enum=["json", "excel"]),
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    perm = Permissions.REPORTS_EXPORT.code if export == "excel" else Permissions.REPORTS_READ.code
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, perm)

    result = ReportService.generate_gst_report(
        db=db,
        pharmacy_id=active_pharmacy_id,
        start_date=start_date,
        end_date=end_date,
        export_excel=(export == "excel"),
    )

    if export == "excel":
        return StreamingResponse(
            result,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=gst_report.xlsx"}
        )
    return result
