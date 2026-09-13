import logging
import secrets

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.base import get_db
from app.provisioning.schemas import ProvisionRequest, ProvisionResponse
from app.provisioning.service import provision

logger = logging.getLogger("medorax-erp.provisioning")

router = APIRouter(
    prefix="/internal/erp",
    tags=["Internal ERP Provisioning"],
)


def require_provision_token(
    authorization: str | None = Header(default=None),
):
    expected = settings.erp_provision_token

    if not expected:
        raise HTTPException(
            status_code=503,
            detail="ERP provisioning token is not configured",
        )

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="ERP provisioning authentication required",
        )

    supplied = authorization[7:].strip()

    if not supplied or not secrets.compare_digest(
        supplied,
        expected,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid ERP provisioning token",
        )


@router.post(
    "/provision",
    response_model=ProvisionResponse,
    dependencies=[Depends(require_provision_token)],
)
def provision_erp(
    payload: ProvisionRequest,
    db: Session = Depends(get_db),
):
    logger.info(
        "ERP provisioning request received: "
        "applicationId=%s pharmacyId=%s username=%s",
        getattr(payload, "applicationId", None),
        payload.pharmacyId,
        payload.erpUsername,
    )

    try:
        user, pharmacy, license_row = provision(
            db,
            payload,
        )

        logger.info(
            "ERP provisioning successful: pharmacyId=%s userId=%s licenseId=%s",
            pharmacy.id,
            user.id,
            license_row.license_id,
        )

        return ProvisionResponse(
            status="provisioned",
            externalId=pharmacy.id,
            userId=user.id,
            pharmacyId=pharmacy.id,
            licenseId=license_row.license_id,
        )

    except HTTPException:
        raise

    except Exception:
        db.rollback()

        logger.exception(
            "ERP provisioning INTERNAL ERROR: pharmacyId=%s username=%s",
            payload.pharmacyId,
            payload.erpUsername,
        )

        raise HTTPException(
            status_code=500,
            detail="ERP provisioning internal error. Check ERP logs.",
        )


@router.get(
    "/health",
    dependencies=[Depends(require_provision_token)],
)
def provisioning_health():
    return {"status": "ok"}
