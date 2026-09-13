import base64
import json
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

import httpx
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.licensing.models import LicenseActivation


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _public_key() -> Ed25519PublicKey:
    pem = os.getenv("LICENSE_PUBLIC_KEY_PEM")
    path = os.getenv("LICENSE_PUBLIC_KEY_FILE") or os.getenv("LICENSE_PUBLIC_KEY_PATH")
    raw = pem.encode() if pem else Path(path).read_bytes() if path else None
    if not raw:
        raise HTTPException(503, "License verification key is not configured")
    try:
        key = serialization.load_pem_public_key(raw)
    except Exception as exc:
        raise HTTPException(503, "Invalid license verification key") from exc
    if not isinstance(key, Ed25519PublicKey):
        raise HTTPException(503, "License verification key must be Ed25519")
    return key


def canonical_payload(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()


def verify_envelope(license_payload: dict[str, Any], signature: str) -> None:
    try:
        padded = signature + "=" * (-len(signature) % 4)
        sig = base64.urlsafe_b64decode(padded.encode())
        _public_key().verify(sig, canonical_payload(license_payload))
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid license signature") from exc


def _expires(value: Any) -> datetime:
    if isinstance(value, int | float):
        return datetime.fromtimestamp(value, timezone.utc)
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    raise HTTPException(400, "License expires_at is invalid")


def validate_payload(payload: dict[str, Any], tenant_id: str) -> tuple[str, datetime, int, list[str]]:
    if not isinstance(payload, dict):
        raise HTTPException(400, "License payload must be an object")
    license_id = str(payload.get("license_id") or "")
    if not license_id:
        raise HTTPException(400, "License license_id is missing")
    if str(payload.get("product", "MEDORAX-ERP")) != "MEDORAX-ERP":
        raise HTTPException(400, "License product is not MEDORAX ERP")
    if str(payload.get("tenant_id")) != str(tenant_id):
        raise HTTPException(403, "License does not belong to this tenant")
    expires_at = _expires(payload.get("expires_at"))
    if expires_at <= _now():
        raise HTTPException(403, "License has expired")
    try:
        max_devices = int(payload.get("max_devices", 1))
    except (TypeError, ValueError) as exc:
        raise HTTPException(400, "License max_devices is invalid") from exc
    if max_devices < 1 or max_devices > 10000:
        raise HTTPException(400, "License max_devices is invalid")
    modules = payload.get("modules", payload.get("features", []))
    if not isinstance(modules, list):
        modules = []
    return license_id, expires_at, max_devices, [str(x) for x in modules]


def _issuer_url() -> str | None:
    return os.getenv("LICENSE_ISSUER_URL", "").rstrip("/") or None

def _issuer_headers() -> dict[str, str]:
    """
    ERP runtime calls use the public licensing protocol.

    The issuer administration token must never be distributed to an ERP
    installation. Issuance/revocation/renewal are control-plane operations
    performed by onboarding/admin. ERP proves possession of a valid signed
    license envelope when activating a device.
    """
    return {}


def issuer_activate(payload: dict[str, Any], signature: str, device_id: str, device_name: str | None) -> dict[str, Any]:
    url = _issuer_url()
    if not url:
        return {"status": "local"}
    try:
        with httpx.Client(timeout=8) as client:
            response = client.post(
                f"{url}/v1/activations",
                json={"license": payload, "signature": signature, "device_id": device_id, "device_name": device_name},
                headers=_issuer_headers(),
            )
        if response.status_code >= 400:
            try:
                detail = response.json().get("detail", "Issuer rejected activation")
            except Exception:
                detail = "Issuer rejected activation"
            raise HTTPException(response.status_code, detail)
        try:
            data = response.json()
        except ValueError as exc:
            raise HTTPException(502, "License issuer returned invalid activation data") from exc
        if not isinstance(data, dict):
            raise HTTPException(502, "License issuer returned invalid activation data")
        return data
    except HTTPException:
        raise
    except httpx.HTTPError as exc:
        raise HTTPException(503, "License issuer unavailable") from exc


def issuer_deactivate(license_id: str, device_id: str) -> None:
    url = _issuer_url()
    if not url:
        return
    try:
        with httpx.Client(timeout=8) as client:
            response = client.post(f"{url}/v1/activations/deactivate", json={"license_id": license_id, "device_id": device_id}, headers=_issuer_headers())
        if response.status_code >= 400:
            raise HTTPException(response.status_code, response.json().get("detail", "Issuer rejected deactivation"))
    except HTTPException:
        raise
    except httpx.HTTPError as exc:
        raise HTTPException(503, "License issuer unavailable") from exc


def issuer_validate(license_id: str, device_id: str) -> dict[str, Any]:
    url = _issuer_url()
    if not url:
        return {"status": "local"}
    try:
        with httpx.Client(timeout=8) as client:
            response = client.post(f"{url}/v1/validate", json={"license_id": license_id, "device_id": device_id}, headers=_issuer_headers())
        if response.status_code >= 400:
            return {"status": "invalid"}
        return response.json()
    except httpx.HTTPError:
        return {"status": "offline"}


def issuer_get_license(license_id: str) -> dict[str, Any]:
    url = _issuer_url()
    if not url:
        raise HTTPException(503, "Central license issuer is not configured")
    try:
        with httpx.Client(timeout=8) as client:
            response = client.get(f"{url}/v1/licenses/{license_id}", headers=_issuer_headers())
        if response.status_code >= 400:
            try:
                detail = response.json().get("detail", "License not found")
            except Exception:
                detail = "License not found"
            raise HTTPException(response.status_code, detail)
        data = response.json()
        payload = data.get("license")
        signature = data.get("signature")
        if not isinstance(payload, dict) or not signature:
            raise HTTPException(502, "License issuer returned an invalid license envelope")
        return {"license": payload, "signature": str(signature)}
    except HTTPException:
        raise
    except httpx.TimeoutException as exc:
        raise HTTPException(503, "License issuer timeout") from exc
    except httpx.HTTPError as exc:
        raise HTTPException(503, "License issuer unavailable") from exc


def activate(db: Session, tenant_id: str, payload: dict[str, Any], signature: str, device_id: str, device_name: str | None):
    verify_envelope(payload, signature)
    license_id, expires_at, max_devices, modules = validate_payload(payload, tenant_id)

    existing = db.query(LicenseActivation).filter(
        LicenseActivation.license_id == license_id,
        LicenseActivation.device_id == device_id,
    ).first()
    if existing:
        existing.status = "active"
        existing.revoked = False
        existing.expires_at = expires_at
        existing.last_validated_at = _now()
        existing.last_heartbeat_at = _now()
        db.flush()
        return existing

    active_count = db.query(func.count(LicenseActivation.id)).filter(
        LicenseActivation.license_id == license_id,
        LicenseActivation.revoked.is_(False),
        LicenseActivation.status == "active",
    ).scalar() or 0
    if active_count >= max_devices:
        raise HTTPException(409, "License device limit reached")

    issuer = issuer_activate(payload, signature, device_id, device_name)
    row = LicenseActivation(
        license_id=license_id,
        tenant_id=tenant_id,
        device_id=device_id,
        device_name=device_name,
        plan=str(payload.get("plan", "standard")),
        status="active",
        max_devices=max_devices,
        expires_at=expires_at,
        modules_json=json.dumps(modules),
        license_payload_json=json.dumps(payload, separators=(",", ":"), sort_keys=True),
        last_validated_at=_now(),
        last_heartbeat_at=_now(),
        issuer_status=str(issuer.get("status", "active")),
    )
    db.add(row)
    db.flush()
    return row


def deactivate(db: Session, tenant_id: str, device_id: str):
    row = db.query(LicenseActivation).filter(
        LicenseActivation.tenant_id == tenant_id,
        LicenseActivation.device_id == device_id,
        LicenseActivation.revoked.is_(False),
    ).first()
    if not row:
        raise HTTPException(404, "Active license device not found")
    issuer_deactivate(row.license_id, device_id)
    row.revoked = True
    row.status = "deactivated"
    row.last_heartbeat_at = _now()
    return row


def status_for_device(db: Session, tenant_id: str, device_id: str | None = None):
    query = db.query(LicenseActivation).filter(LicenseActivation.tenant_id == tenant_id)
    if device_id:
        query = query.filter(LicenseActivation.device_id == device_id)
    row = query.order_by(LicenseActivation.updated_at.desc()).first()
    if not row:
        return None
    issuer = issuer_validate(row.license_id, row.device_id)
    issuer_status = issuer.get("status")
    if issuer_status:
        row.issuer_status = issuer_status

    # Only a successful online validation advances the offline grace clock.
    # Otherwise an outage could extend grace indefinitely by repeatedly calling
    # the status endpoint.
    if issuer_status == "active":
        row.last_validated_at = _now()
        row.last_heartbeat_at = _now()
    elif issuer_status == "revoked":
        row.revoked = True
        row.status = "revoked"

    if row.expires_at <= _now():
        row.status = "expired"
    return row


def to_status(row: LicenseActivation | None) -> dict[str, Any]:
    if not row:
        return {"license_id": None, "tenant_id": None, "plan": None, "status": "unlicensed", "expires_at": None, "max_devices": None, "modules": [], "device_id": None, "issuer_status": None, "offline_valid_until": None}
    try:
        modules = json.loads(row.modules_json or "[]")
    except (TypeError, ValueError):
        modules = []
    if not isinstance(modules, list):
        modules = []
    offline_hours = int(os.getenv("LICENSE_OFFLINE_GRACE_HOURS", "24"))
    offline_until = min(row.expires_at, (row.last_validated_at or row.created_at or _now()) + timedelta(hours=offline_hours))
    return {"license_id": row.license_id, "tenant_id": row.tenant_id, "plan": row.plan, "status": row.status if not row.revoked else "revoked", "expires_at": row.expires_at, "max_devices": row.max_devices, "modules": modules, "device_id": row.device_id, "issuer_status": row.issuer_status, "offline_valid_until": offline_until}


def ensure_login_license(db: Session, user, device_id: str, device_name: str | None = None):
    """Require and, on first login, activate the tenant's provisioned license."""
    from app.pharmacy.models import PharmacyOwner
    from app.provisioning.models import ProvisionedLicense
    owner = db.query(PharmacyOwner).filter(PharmacyOwner.user_id == user.id).first()
    if not owner: raise HTTPException(403, "ERP access is not provisioned for this account")
    tenant = str(owner.pharmacy_id)
    provisioned = db.query(ProvisionedLicense).filter(ProvisionedLicense.tenant_id == tenant, ProvisionedLicense.status == "active").first()
    if not provisioned: raise HTTPException(403, "MEDORAX ERP license is not provisioned for this account")
    if provisioned.expires_at <= _now():
        provisioned.status = "expired"; db.commit(); raise HTTPException(403, "MEDORAX ERP license has expired")
    try:
        payload = json.loads(provisioned.license_json)
    except (TypeError, ValueError) as exc:
        raise HTTPException(500, "Provisioned license data is corrupt") from exc
    license_id, _, _, _ = validate_payload(payload, tenant)
    if license_id != provisioned.license_id: raise HTTPException(403, "Provisioned license is inconsistent")
    existing = db.query(LicenseActivation).filter(LicenseActivation.license_id == license_id, LicenseActivation.tenant_id == tenant, LicenseActivation.device_id == device_id, LicenseActivation.revoked.is_(False)).first()
    if existing:
        state = status_for_device(db, tenant, device_id)
        if not state or state.revoked or state.status == "expired":
            db.commit(); raise HTTPException(403, "MEDORAX ERP license is not active")
        db.commit(); return state
    row = activate(db, tenant, payload, provisioned.signature, device_id, device_name)
    db.commit()
    state = status_for_device(db, tenant, device_id)
    if not state or state.revoked or state.status == "expired":
        db.rollback(); raise HTTPException(403, "MEDORAX ERP license validation failed")
    db.commit(); return state
