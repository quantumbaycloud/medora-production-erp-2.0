import secrets

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.base import get_db
from app.provisioning.schemas import ProvisionRequest, ProvisionResponse
from app.provisioning.service import provision

router = APIRouter(prefix="/internal/erp", tags=["Internal ERP Provisioning"])


def require_provision_token(authorization: str | None = Header(default=None)):
    expected = settings.erp_provision_token
    if not expected:
        raise HTTPException(503, "ERP provisioning token is not configured")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "ERP provisioning authentication required")
    supplied = authorization[7:].strip()
    if not supplied or not secrets.compare_digest(supplied, expected):
        raise HTTPException(401, "Invalid ERP provisioning token")


@router.post("/provision", response_model=ProvisionResponse, dependencies=[Depends(require_provision_token)])
def provision_erp(payload: ProvisionRequest, db: Session = Depends(get_db)):
    user, pharmacy, license_row = provision(db, payload)
    return ProvisionResponse(
        status="provisioned",
        externalId=pharmacy.id,
        userId=user.id,
        pharmacyId=pharmacy.id,
        licenseId=license_row.license_id,
    )


@router.get("/health", dependencies=[Depends(require_provision_token)])
def provisioning_health():
    return {"status": "ok"}
