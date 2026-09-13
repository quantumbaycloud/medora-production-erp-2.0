import json

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.catalog.models import CatalogOption
from app.catalog.schemas import CatalogOptionCreate
from app.db.base import get_db
from app.licensing.deps import get_current_licensed_user
from app.staff.service import get_current_pharmacy_id
from app.user.models import User

from app.admin_sync.service import (
    OPTION_TYPES,
    normalize_catalog_items,
    pull_catalog_from_admin,
)

router = APIRouter(prefix="/admin-sync", tags=["Admin Sync"])


@router.post("/catalog")
async def sync_catalog(
    pharmacy_id: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user),
):
    active = get_current_pharmacy_id(
        db,
        current_user.id,
        pharmacy_id,
    )

    payload = await pull_catalog_from_admin(db, active)
    items = normalize_catalog_items(payload)

    incoming_keys = set()
    created = 0
    updated = 0
    disabled = 0

    for item in items:
        key = (item["option_type"], item["code"])
        incoming_keys.add(key)

        row = (
            db.query(CatalogOption)
            .filter(
                CatalogOption.pharmacy_id == active,
                CatalogOption.option_type == item["option_type"],
                CatalogOption.code == item["code"],
            )
            .first()
        )

        if row is None:
            row = CatalogOption(
                pharmacy_id=active,
                option_type=item["option_type"],
                code=item["code"],
                name=item["name"],
                is_active=item["is_active"],
                sort_order=item["sort_order"],
                metadata_json=(
                    json.dumps(item["metadata"], separators=(",", ":"), sort_keys=True)
                    if item["metadata"] is not None
                    else None
                ),
            )
            db.add(row)
            created += 1
            continue

        row.name = item["name"]
        row.is_active = item["is_active"]
        row.sort_order = item["sort_order"]
        row.metadata_json = (
            json.dumps(item["metadata"], separators=(",", ":"), sort_keys=True)
            if item["metadata"] is not None
            else None
        )
        updated += 1

    # The Admin catalog is authoritative. Deactivate previously synced options
    # that are no longer present, without deleting historical master data.
    existing = (
        db.query(CatalogOption)
        .filter(CatalogOption.pharmacy_id == active)
        .all()
    )

    for row in existing:
        if (row.option_type, row.code) in incoming_keys:
            continue
        if row.option_type in OPTION_TYPES and row.is_active:
            row.is_active = False
            disabled += 1

    db.commit()

    return {
        "status": "synced",
        "pharmacy_id": active,
        "received": len(items),
        "created": created,
        "updated": updated,
        "disabled": disabled,
        "changed": created + updated + disabled,
    }
