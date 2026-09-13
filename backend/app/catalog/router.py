from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.licensing.deps import get_current_licensed_user
from app.staff.permissions import Permissions
from app.staff.service import get_current_pharmacy_id
from app.user.models import User
from app.catalog.schemas import CatalogOptionCreate, CatalogOptionUpdate
from app.catalog.service import CatalogService

router = APIRouter(prefix="/catalog", tags=["ERP Catalog"])

@router.get("")
def list_catalog(option_type: str | None = Query(None), include_inactive: bool = False,
                 pharmacy_id: str | None = Query(None), db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_licensed_user)):
    active = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.SETTINGS_UPDATE.code)
    rows = CatalogService.list(db, active, option_type, not include_inactive)
    return [CatalogService.as_dict(r) for r in rows]

@router.post("", status_code=status.HTTP_201_CREATED)
def create_catalog(data: CatalogOptionCreate, pharmacy_id: str | None = Query(None),
                   db: Session = Depends(get_db), current_user: User = Depends(get_current_licensed_user)):
    active = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.SETTINGS_UPDATE.code)
    return CatalogService.as_dict(CatalogService.create(db, active, data))

@router.patch("/{option_id}")
def update_catalog(option_id: str, data: CatalogOptionUpdate, pharmacy_id: str | None = Query(None),
                   db: Session = Depends(get_db), current_user: User = Depends(get_current_licensed_user)):
    active = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.SETTINGS_UPDATE.code)
    return CatalogService.as_dict(CatalogService.update(db, active, option_id, data))

@router.delete("/{option_id}", status_code=204)
def delete_catalog(option_id: str, pharmacy_id: str | None = Query(None),
                   db: Session = Depends(get_db), current_user: User = Depends(get_current_licensed_user)):
    active = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.SETTINGS_UPDATE.code)
    CatalogService.delete(db, active, option_id)
