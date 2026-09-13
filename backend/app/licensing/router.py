import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.licensing import service
from app.licensing.schemas import ActivationRequest, DeactivationRequest, LicenseKeyActivationRequest
from app.provisioning.models import ProvisionedLicense
from app.pharmacy.models import PharmacyOwner
from app.shared.deps import get_current_user
from app.user.models import User

router = APIRouter(prefix="/api/licensing", tags=["licensing"])

class BootstrapDeviceRequest(BaseModel):
    device_id: str = Field(min_length=8, max_length=255)
    device_name: str | None = Field(default=None, max_length=255)

def _tenant(db: Session, current_user: User, tenant_id: str | None) -> str:
    if tenant_id:
        allowed = db.query(PharmacyOwner).filter(PharmacyOwner.user_id == current_user.id, PharmacyOwner.pharmacy_id == tenant_id).first()
        if not allowed:
            raise HTTPException(403, "You do not have access to this pharmacy")
        return tenant_id
    owner = db.query(PharmacyOwner).filter(PharmacyOwner.user_id == current_user.id).first()
    if not owner:
        raise HTTPException(400, "No pharmacy is provisioned for this account")
    return owner.pharmacy_id

def _session_device(db: Session, current_user: User) -> str:
    from app.auth.models import Session as AuthSession
    session_id = getattr(current_user, "_current_session_id", None)
    row = db.query(AuthSession).filter(AuthSession.id == session_id).first() if session_id else None
    device_id = row.device.device_identifier if row and row.device else None
    if not device_id:
        raise HTTPException(403, "ERP device identity is unavailable")
    return device_id

def _require_current_device(db: Session, current_user: User, requested: str | None = None) -> str:
    current = _session_device(db, current_user)
    if requested and requested != current:
        raise HTTPException(403, "License operations are restricted to the current ERP device")
    return current

@router.post("/activate")
def activate(request: ActivationRequest, tenant_id: str | None = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tenant = _tenant(db, current_user, tenant_id)
    device_id = _require_current_device(db, current_user, request.device_id)
    row = service.activate(db, tenant, request.license, request.signature, device_id, request.device_name)
    db.commit()
    return {"status": "active", "license": service.to_status(row)}

@router.post("/activate-key")
def activate_by_key(request: LicenseKeyActivationRequest, tenant_id: str | None = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tenant = _tenant(db, current_user, tenant_id)
    device_id = _session_device(db, current_user)
    envelope = service.issuer_get_license(request.license_key.strip())
    payload = envelope["license"]
    if str(payload.get("license_id")) != request.license_key.strip():
        raise HTTPException(502, "License issuer returned a mismatched license key")
    row = service.activate(db, tenant, payload, envelope["signature"], device_id, "Web Browser")
    db.commit()
    return {"status": "active", "license": service.to_status(row)}

@router.post("/bootstrap-device")
def bootstrap_device(request: BootstrapDeviceRequest, tenant_id: str | None = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tenant = _tenant(db, current_user, tenant_id)
    provisioned = db.query(ProvisionedLicense).filter(ProvisionedLicense.tenant_id == tenant, ProvisionedLicense.status == "active").first()
    if not provisioned:
        raise HTTPException(404, "No provisioned MEDORAX ERP license found")
    if provisioned.expires_at <= service._now():
        provisioned.status = "expired"
        db.commit()
        raise HTTPException(403, "Provisioned MEDORAX ERP license has expired")
    payload = json.loads(provisioned.license_json)
    device_id = _require_current_device(db, current_user, request.device_id)
    row = service.activate(db, tenant, payload, provisioned.signature, device_id, request.device_name)
    db.commit()
    return {"status": "active", "license": service.to_status(row)}

@router.get("/provisioned")
def provisioned(tenant_id: str | None = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tenant = _tenant(db, current_user, tenant_id)
    row = db.query(ProvisionedLicense).filter(ProvisionedLicense.tenant_id == tenant, ProvisionedLicense.status == "active").first()
    if not row:
        return {"status": "unlicensed", "license_id": None, "expires_at": None, "plan": None}
    if row.expires_at <= service._now():
        row.status = "expired"
        db.commit()
        return {"status": "expired", "license_id": row.license_id, "expires_at": row.expires_at, "plan": row.plan}
    return {"status": "provisioned", "license_id": row.license_id, "expires_at": row.expires_at, "plan": row.plan}

@router.post("/deactivate")
def deactivate(request: DeactivationRequest, tenant_id: str | None = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tenant = _tenant(db, current_user, tenant_id)
    device_id = _require_current_device(db, current_user, request.device_id)
    row = service.deactivate(db, tenant, device_id)
    db.commit()
    return {"status": "deactivated", "license": service.to_status(row)}

@router.post("/validate")
def validate(tenant_id: str | None = None, device_id: str | None = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tenant = _tenant(db, current_user, tenant_id)
    current_device = _require_current_device(db, current_user, device_id)
    return service.to_status(service.status_for_device(db, tenant, current_device))

@router.post("/refresh")
def refresh(tenant_id: str | None = None, device_id: str | None = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tenant = _tenant(db, current_user, tenant_id)
    current_device = _require_current_device(db, current_user, device_id)
    return service.to_status(service.status_for_device(db, tenant, current_device))

@router.get("/status")
def status(tenant_id: str | None = None, device_id: str | None = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tenant = _tenant(db, current_user, tenant_id)
    current_device = _require_current_device(db, current_user, device_id)
    return service.to_status(service.status_for_device(db, tenant, current_device))

@router.get("/modules")
def modules(tenant_id: str | None = None, device_id: str | None = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tenant = _tenant(db, current_user, tenant_id)
    current_device = _require_current_device(db, current_user, device_id)
    data = service.to_status(service.status_for_device(db, tenant, current_device))
    return {"license_id": data["license_id"], "plan": data["plan"], "modules": data["modules"], "status": data["status"]}
