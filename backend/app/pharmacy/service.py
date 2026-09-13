from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.pharmacy.models import Pharmacy, PharmacyOwner
from app.pharmacy.schemas import PharmacyCreate, PharmacyUpdate
from app.services.audit import audit_log


def _check_duplicate_gst(db: Session, gst_number: str | None, ignore_pharmacy_id: str | None = None) -> None:
    if not gst_number:
        return
    gst_number = gst_number.strip().upper()
    query = db.query(Pharmacy.id).filter(Pharmacy.gst_number == gst_number)
    if ignore_pharmacy_id:
        query = query.filter(Pharmacy.id != ignore_pharmacy_id)
    if query.first():
        raise HTTPException(status.HTTP_409_CONFLICT, "A pharmacy with this GST number already exists")


def create_pharmacy(db: Session, owner_user_id: str, payload: PharmacyCreate) -> Pharmacy:
    _check_duplicate_gst(db, payload.gst_number)
    pharmacy = Pharmacy(owner_user_id=owner_user_id, **payload.model_dump())
    db.add(pharmacy)
    db.flush()
    db.add(PharmacyOwner(pharmacy_id=pharmacy.id, user_id=owner_user_id))
    db.commit()
    db.refresh(pharmacy)
    audit_log("PHARMACY_CREATED", user_id=owner_user_id, pharmacy_id=pharmacy.id, pharmacy_name=pharmacy.name)
    return pharmacy


def get_pharmacy(db: Session, pharmacy_id: str) -> Pharmacy | None:
    return db.query(Pharmacy).filter(Pharmacy.id == pharmacy_id).first()


def get_pharmacy_or_404(db: Session, pharmacy_id: str) -> Pharmacy:
    pharmacy = get_pharmacy(db, pharmacy_id)
    if not pharmacy:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pharmacy not found")
    return pharmacy


def list_pharmacies_for_owner(db: Session, owner_user_id: str, skip: int = 0, limit: int = 100) -> list[Pharmacy]:
    return (
        db.query(Pharmacy)
        .join(PharmacyOwner, PharmacyOwner.pharmacy_id == Pharmacy.id)
        .filter(PharmacyOwner.user_id == owner_user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_pharmacy(db: Session, pharmacy: Pharmacy, payload: PharmacyUpdate) -> Pharmacy:
    updates = payload.model_dump(exclude_unset=True)
    if "gst_number" in updates and updates["gst_number"]:
        _check_duplicate_gst(db, updates["gst_number"], ignore_pharmacy_id=pharmacy.id)
    for field, value in updates.items():
        setattr(pharmacy, field, value)
    db.commit()
    db.refresh(pharmacy)
    audit_log("PHARMACY_UPDATED", pharmacy_id=pharmacy.id, updated_fields=list(updates.keys()))
    return pharmacy


def assert_is_owner(db: Session, pharmacy: Pharmacy, user_id: str) -> None:
    is_owner = (
        db.query(PharmacyOwner.pharmacy_id)
        .filter(PharmacyOwner.pharmacy_id == pharmacy.id, PharmacyOwner.user_id == user_id)
        .first()
    )
    if not is_owner:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only the pharmacy owner can do this")
