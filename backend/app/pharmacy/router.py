from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from app.db.base import get_db
from app.pharmacy import service
from app.pharmacy.schemas import PharmacyCreate, PharmacyRead, PharmacyUpdate
from app.licensing.deps import get_current_licensed_user
from app.user.models import User

# Router-level auth: every route here requires a logged-in user.
# Endpoint-level authorization (ownership) is checked per-route below,
# per your Section 13/14 decision (router = authN, endpoint = authZ).
router = APIRouter(prefix="/pharmacies", tags=["pharmacy"])


@router.post(
    "",
    response_model=PharmacyRead,
    status_code=201,
    summary="Create a new pharmacy profile",
    description="Create a pharmacy business profile. The authenticated user automatically becomes the primary owner.",
    responses={
        400: {"description": "Invalid input"},
        401: {"description": "Authentication required"},
        409: {"description": "Duplicate GST number"},
        422: {"description": "Validation error"},
    },
)
def create_pharmacy(
    payload: PharmacyCreate,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    return service.create_pharmacy(db, current_user.id, payload)


@router.get(
    "/mine",
    response_model=list[PharmacyRead],
    summary="List owned pharmacies",
    description="Retrieve all pharmacy profiles owned by the currently authenticated user.",
    responses={
        401: {"description": "Authentication required"},
    },
)
def list_my_pharmacies(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    return service.list_pharmacies_for_owner(db, current_user.id, skip=skip, limit=limit)


@router.get(
    "/{pharmacy_id}",
    response_model=PharmacyRead,
    summary="Get pharmacy by ID",
    description="Retrieve a pharmacy profile by ID. Only the pharmacy owner is authorized to view it.",
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Not authorized to access this pharmacy"},
        404: {"description": "Pharmacy not found"},
    },
)
def read_pharmacy(
    pharmacy_id: str,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    pharmacy = service.get_pharmacy_or_404(db, pharmacy_id)
    service.assert_is_owner(db, pharmacy, current_user.id)
    return pharmacy


@router.patch(
    "/{pharmacy_id}",
    response_model=PharmacyRead,
    summary="Update pharmacy profile",
    description="Update non-null fields of a pharmacy profile. Requires owner authorization.",
    responses={
        400: {"description": "Invalid input"},
        401: {"description": "Authentication required"},
        403: {"description": "Not authorized to update this pharmacy"},
        404: {"description": "Pharmacy not found"},
        409: {"description": "Duplicate GST number"},
        422: {"description": "Validation error"},
    },
)
def update_pharmacy(
    pharmacy_id: str,
    payload: PharmacyUpdate,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    pharmacy = service.get_pharmacy_or_404(db, pharmacy_id)
    service.assert_is_owner(db, pharmacy, current_user.id)
    return service.update_pharmacy(db, pharmacy, payload)
