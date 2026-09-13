from datetime import datetime, timezone
import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth.models import Credential, Session as AuthSession
from app.core.security import hash_password
from app.pharmacy.models import Pharmacy, PharmacyOwner
from app.provisioning.models import ProvisionedLicense
from app.provisioning.schemas import ProvisionRequest
from app.user.models import User


def _dt(value):
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, timezone.utc)
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    raise HTTPException(400, "licenseExpiresAt is invalid")


def provision(db: Session, payload: ProvisionRequest):
    expires_at = _dt(payload.licenseExpiresAt)
    if expires_at <= datetime.now(timezone.utc):
        raise HTTPException(400, "License has expired")

    license_payload = dict(payload.license)
    if str(license_payload.get("license_id")) != payload.licenseKey:
        raise HTTPException(400, "licenseKey does not match license payload")

    payload_expires_at = _dt(license_payload.get("expires_at"))
    if payload_expires_at != expires_at:
        raise HTTPException(400, "licenseExpiresAt does not match signed license")
    if str(license_payload.get("tenant_id")) != payload.pharmacyId:
        raise HTTPException(400, "License tenant does not match pharmacyId")
    if str(license_payload.get("product", "MEDORAX-ERP")) != "MEDORAX-ERP":
        raise HTTPException(400, "License product is invalid")

    from app.licensing.service import validate_payload, verify_envelope
    validate_payload(license_payload, payload.pharmacyId)
    verify_envelope(license_payload, payload.licenseSignature)

    email = (payload.user.email or "").strip().lower() or None
    phone = (payload.user.phone or "").strip() or None
    username = payload.erpUsername.strip().lower()

    existing_username = db.query(User).filter(User.username == username).first()
    user = db.query(User).filter(User.email == email).first() if email else None
    if user is None and phone:
        user = db.query(User).filter(User.phone == phone).first()

    if existing_username and (user is None or existing_username.id != user.id):
        raise HTTPException(409, "ERP username is already assigned to another account")

    now = datetime.now(timezone.utc)

    if user is None:
        user = User(
            name=payload.user.name or payload.erpUsername,
            username=username,
            email=email,
            phone=phone,
            email_verified=True,
            phone_verified=bool(phone),
            is_active=True,
        )
        db.add(user)
        db.flush()
    else:
        user.is_active = True
        user.email_verified = True
        user.username = username
        if payload.user.name:
            user.name = payload.user.name

    credential = db.query(Credential).filter(Credential.user_id == user.id).first()
    password_hash = hash_password(payload.temporaryPassword)
    if credential is None:
        db.add(Credential(user_id=user.id, password_hash=password_hash))
    else:
        credential.password_hash = password_hash

    # Provisioning is authoritative for onboarding-created ERP credentials.
    # Any prior ERP session is invalid after a credential rotation.
    user.password_updated_at = now
    db.query(AuthSession).filter(
        AuthSession.user_id == user.id,
        AuthSession.revoked.is_(False),
    ).update(
        {
            "revoked": True,
            "revoked_at": now,
            "logout_reason": "credential_rotated_by_onboarding",
        },
        synchronize_session=False,
    )

    pharmacy = db.query(Pharmacy).filter(Pharmacy.id == payload.pharmacyId).first()
    if pharmacy is None:
        pharmacy = Pharmacy(
            id=payload.pharmacyId,
            owner_user_id=user.id,
            name=payload.business.name,
            gst_number=payload.business.gst_number,
            pan_number=payload.business.pan_number,
            address=payload.business.address,
            contact_phone=payload.business.contact_phone,
            contact_email=payload.business.contact_email or email,
            bank_account_number=payload.business.bank_account_number,
            bank_ifsc=payload.business.bank_ifsc,
            bank_name=payload.business.bank_name,
        )
        db.add(pharmacy)
        db.flush()
    else:
        pharmacy.owner_user_id = user.id
        pharmacy.name = payload.business.name or pharmacy.name
        for field in (
            "gst_number", "pan_number", "address", "contact_phone",
            "contact_email", "bank_account_number", "bank_ifsc", "bank_name",
        ):
            value = getattr(payload.business, field)
            if value is not None:
                setattr(pharmacy, field, value)

    membership = db.query(PharmacyOwner).filter(
        PharmacyOwner.pharmacy_id == pharmacy.id,
        PharmacyOwner.user_id == user.id,
    ).first()
    if membership is None:
        db.add(PharmacyOwner(pharmacy_id=pharmacy.id, user_id=user.id))

    row = db.query(ProvisionedLicense).filter(
        ProvisionedLicense.tenant_id == payload.pharmacyId
    ).first()
    encoded = json.dumps(license_payload, separators=(",", ":"), sort_keys=True)

    if row is None:
        row = ProvisionedLicense(
            tenant_id=payload.pharmacyId,
            license_id=payload.licenseKey,
            plan=str(license_payload.get("plan", "standard")),
            expires_at=expires_at,
            license_json=encoded,
            signature=payload.licenseSignature,
            status="active",
        )
        db.add(row)
    else:
        row.license_id = payload.licenseKey
        row.plan = str(license_payload.get("plan", row.plan))
        row.expires_at = expires_at
        row.license_json = encoded
        row.signature = payload.licenseSignature
        row.status = "active"

    db.commit()
    db.refresh(user)
    db.refresh(pharmacy)
    db.refresh(row)
    return user, pharmacy, row
