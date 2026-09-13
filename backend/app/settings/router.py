from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Optional

from app.db.base import get_db
from app.licensing.deps import get_current_licensed_user
from app.user.models import User
from app.staff.service import get_current_pharmacy_id
from app.staff.permissions import Permissions
from app.settings.schemas import SettingResponse, SettingUpdate
from app.settings.service import SettingService

router = APIRouter(prefix="/settings", tags=["Pharmacy Settings"])


@router.get("", response_model=SettingResponse)
def get_settings(
    pharmacy_id: Optional[str] = Query(
        None,
        description="Optional Pharmacy ID context"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user),
):
    active_pharmacy_id = get_current_pharmacy_id(
        db,
        current_user.id,
        pharmacy_id,
        Permissions.SETTINGS_UPDATE.code,
    )

    return SettingService.get_or_create_settings(
        db,
        active_pharmacy_id,
    )


@router.patch("", response_model=SettingResponse)
@router.put("", response_model=SettingResponse)
def update_settings(
    data: SettingUpdate,
    request: Request,
    pharmacy_id: Optional[str] = Query(
        None,
        description="Optional Pharmacy ID context"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user),
):
    active_pharmacy_id = get_current_pharmacy_id(
        db,
        current_user.id,
        pharmacy_id,
        Permissions.SETTINGS_UPDATE.code,
    )

    client_ip = request.client.host if request.client else "unknown"

    return SettingService.update_settings(
        db=db,
        pharmacy_id=active_pharmacy_id,
        user_id=current_user.id,
        user_email=current_user.email or "unknown",
        data=data,
        ip_address=client_ip,
    )