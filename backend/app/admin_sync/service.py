import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.config import settings
from app.provisioning.models import ProvisionedLicense

async def pull_catalog_from_admin(db: Session, pharmacy_id: str):
    if not settings.admin_sync_url:
        return {"status": "disabled", "items": []}
    license_row = db.query(ProvisionedLicense).filter(
        ProvisionedLicense.tenant_id == pharmacy_id,
        ProvisionedLicense.status == "active",
    ).first()
    if not license_row:
        raise HTTPException(403, "Active ERP license not found")
    url = settings.admin_sync_url.rstrip("/") + f"/erp-sync/{pharmacy_id}/catalog"
    try:
        async with httpx.AsyncClient(timeout=settings.admin_sync_timeout_seconds) as client:
            response = await client.get(url, headers={
                "X-ERP-License-Key": license_row.license_id,
                "X-ERP-License-Signature": license_row.signature,
            })
    except httpx.HTTPError as exc:
        raise HTTPException(503, "Medorax Admin sync service unavailable") from exc
    if response.status_code >= 400:
        try: detail = response.json().get("detail", "Admin rejected ERP sync")
        except Exception: detail = "Admin rejected ERP sync"
        raise HTTPException(response.status_code, detail)
    return response.json()
