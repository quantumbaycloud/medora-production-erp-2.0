"""Dependencies for enforcing the commercial MEDORAX ERP license."""
from datetime import datetime, timezone, timedelta

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.base import get_db
from app.auth.models import Session as AuthSession
from app.licensing import service
from app.pharmacy.models import PharmacyOwner
from app.shared.deps import get_current_user
from app.user.models import User


def get_current_licensed_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Require an authenticated user with an active commercial ERP license.

    The user must belong to a pharmacy, and that pharmacy must have an active
    device activation. Issuer validation is performed by status_for_device().
    During an issuer outage, the existing last successful validation is honored
    only for LICENSE_OFFLINE_GRACE_HOURS.
    """
    owner = (
        db.query(PharmacyOwner)
        .filter(PharmacyOwner.user_id == current_user.id)
        .first()
    )
    if not owner:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "ERP access requires a provisioned pharmacy")

    session_id = getattr(current_user, "_current_session_id", None)
    session = db.query(AuthSession).filter(AuthSession.id == session_id).first() if session_id else None
    device_id = session.device.device_identifier if session and session.device else None
    if not device_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "ERP device identity is unavailable")

    row = service.status_for_device(db, owner.pharmacy_id, device_id)
    if not row:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "MEDORAX ERP license is not activated on this device")

    now = datetime.now(timezone.utc)
    if row.revoked or row.status in {"revoked", "deactivated", "expired", "inactive"}:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "MEDORAX ERP license is not active")
    if row.expires_at <= now:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "MEDORAX ERP license has expired")

    # Persist successful online validation / revocation / expiry transitions.
    db.commit()

    issuer_status = (row.issuer_status or "").lower()
    if issuer_status in {"revoked", "invalid", "expired", "inactive"}:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "MEDORAX ERP license is not valid")

    if issuer_status == "offline":
        last = row.last_validated_at
        if not last:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "License issuer unavailable")
        grace_until = min(
            row.expires_at,
            last + timedelta(hours=settings.license_offline_grace_hours),
        )
        if now >= grace_until:
            raise HTTPException(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                "License issuer unavailable and offline grace period has expired",
            )

    return current_user
