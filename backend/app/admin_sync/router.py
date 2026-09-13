from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.licensing.deps import get_current_licensed_user
from app.staff.service import get_current_pharmacy_id
from app.staff.permissions import Permissions
from app.user.models import User
from app.catalog.models import CatalogOption
from app.catalog.schemas import CatalogOptionCreate
from app.admin_sync.service import pull_catalog_from_admin

router = APIRouter(prefix="/admin-sync", tags=["Admin Sync"])

@router.post("/catalog")
async def sync_catalog(pharmacy_id: str | None = Query(None),
                        db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_licensed_user)):
    active = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.SETTINGS_UPDATE.code)
    payload = await pull_catalog_from_admin(db, active)
    items = payload.get("items", [])
    changed = 0
    for item in items:
        if item.get("option_type") not in {"supplier_category", "medicine_category", "payment_term", "customer_type", "dosage_form", "unit"}:
            continue
        row = db.query(CatalogOption).filter(
            CatalogOption.pharmacy_id == active,
            CatalogOption.option_type == item["option_type"],
            CatalogOption.code == item["code"],
        ).first()
        if not row:
            row = CatalogOption(pharmacy_id=active, option_type=item["option_type"], code=item["code"], name=item["name"],
                                is_active=item.get("is_active", True), sort_order=item.get("sort_order", 0))
            db.add(row); changed += 1
        else:
            row.name = item["name"]; row.is_active = item.get("is_active", True); row.sort_order = item.get("sort_order", 0); changed += 1
    db.flush()
    return {"status": "synced", "pharmacy_id": active, "received": len(items), "changed": changed}
