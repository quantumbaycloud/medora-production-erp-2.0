from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.base import get_db
from app.licensing.deps import get_current_licensed_user
from app.user.models import User
from app.staff.service import get_current_pharmacy_id
from app.staff.permissions import Permissions
from app.notifications.schemas import NotificationResponse
from app.notifications.service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications & Alerts"])

@router.get("", response_model=List[NotificationResponse])
def get_notifications(
    unread_only: bool = Query(False),
    limit: int = Query(50, ge=1, le=100),
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.NOTIFICATION_READ.code)
    return NotificationService.list_notifications(db, active_pharmacy_id, unread_only=unread_only, limit=limit)

@router.patch("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_read(
    notification_id: str,
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.NOTIFICATION_MANAGE.code)
    return NotificationService.mark_as_read(db, active_pharmacy_id, notification_id)

@router.post("/mark-all-read")
def mark_all_notifications_read(
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.NOTIFICATION_MANAGE.code)
    count = NotificationService.mark_all_as_read(db, active_pharmacy_id)
    return {"status": "success", "marked_read_count": count}
