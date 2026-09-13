import json
import logging
from datetime import datetime, timezone

import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.provisioning.models import ProvisionedLicense

logger = logging.getLogger("medorax-erp.admin-sync")

OPTION_TYPES = {
    "supplier_category",
    "medicine_category",
    "payment_term",
    "customer_type",
    "dosage_form",
    "unit",
}


def _active_license(db: Session, pharmacy_id: str) -> ProvisionedLicense:
    row = (
        db.query(ProvisionedLicense)
        .filter(
            ProvisionedLicense.tenant_id == pharmacy_id,
            ProvisionedLicense.status == "active",
        )
        .first()
    )
    if not row:
        raise HTTPException(403, "Active ERP license not found")
    expires_at = row.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

if expires_at <= datetime.now(timezone.utc):
    row.    status = "expired"
    db.commit()
    raise HTTPException(403, "MEDORAX ERP license has expired")
    if not row.license_id or not row.signature:
        raise HTTPException(403, "Installed ERP license envelope is incomplete")
    return row


async def pull_catalog_from_admin(db: Session, pharmacy_id: str):
    """
    Pull pharmacy-scoped ERP master data from the central Admin control plane.

    This is an outbound ERP -> Admin call, so it works even when the local
    ERP is behind NAT or its inbound Cloudflare tunnel is unavailable.
    """
    if not settings.admin_sync_url:
        return {"status": "disabled", "pharmacyId": pharmacy_id, "options": []}

    license_row = _active_license(db, pharmacy_id)
    url = settings.admin_sync_url.rstrip("/") + f"/erp-sync/{pharmacy_id}/catalog"

    headers = {
        "Accept": "application/json",
        "X-ERP-License-Key": license_row.license_id,
        "X-ERP-License-Signature": license_row.signature,
    }

    try:
        async with httpx.AsyncClient(
            timeout=settings.admin_sync_timeout_seconds,
            follow_redirects=False,
        ) as client:
            response = await client.post(url, headers=headers)
    except httpx.TimeoutException as exc:
        logger.warning("Admin catalog sync timeout pharmacy_id=%s", pharmacy_id)
        raise HTTPException(503, "Medorax Admin sync service timed out") from exc
    except httpx.HTTPError as exc:
        logger.warning("Admin catalog sync unavailable pharmacy_id=%s error=%s", pharmacy_id, exc)
        raise HTTPException(503, "Medorax Admin sync service unavailable") from exc

    if response.status_code >= 400:
        try:
            body = response.json()
            detail = body.get("detail", "Admin rejected ERP sync")
        except Exception:
            detail = "Admin rejected ERP sync"
        raise HTTPException(response.status_code, str(detail))

    try:
        payload = response.json()
    except ValueError as exc:
        raise HTTPException(502, "Admin returned invalid ERP catalog data") from exc

    if not isinstance(payload, dict):
        raise HTTPException(502, "Admin returned invalid ERP catalog data")

    returned_pharmacy = str(
        payload.get("pharmacyId")
        or payload.get("pharmacy_id")
        or pharmacy_id
    )
    if returned_pharmacy != str(pharmacy_id):
        raise HTTPException(502, "Admin returned catalog for the wrong pharmacy")

    return payload


def normalize_catalog_items(payload: dict) -> list[dict]:
    """Normalize Admin's API representation into the ERP catalog contract."""
    raw_items = payload.get("options")
    if raw_items is None:
        raw_items = payload.get("items", [])

    if not isinstance(raw_items, list):
        raise HTTPException(502, "Admin returned an invalid catalog list")

    items = []
    for item in raw_items:
        if not isinstance(item, dict):
            continue

        option_type = item.get("optionType") or item.get("option_type")
        code = item.get("code")
        name = item.get("name")

        if option_type not in OPTION_TYPES or not code or not name:
            continue

        metadata = item.get("metadata")
        items.append(
            {
                "id": str(item.get("id")) if item.get("id") is not None else None,
                "option_type": str(option_type),
                "code": str(code).strip().lower().replace(" ", "-"),
                "name": str(name).strip(),
                "is_active": bool(
                    item.get("isActive")
                    if item.get("isActive") is not None
                    else item.get("is_active", True)
                ),
                "sort_order": int(
                    item.get("sortOrder")
                    if item.get("sortOrder") is not None
                    else item.get("sort_order", 0)
                ),
                "metadata": metadata if isinstance(metadata, dict) else None,
            }
        )

    return items
