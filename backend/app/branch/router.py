from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from app.branch import service
from app.branch.schemas import BranchCreate, BranchRead, BranchStatusUpdate, BranchUpdate
from app.db.base import get_db
from app.pharmacy import service as pharmacy_service
from app.licensing.deps import get_current_licensed_user
from app.user.models import User

# Router-level auth (Section 13/14): every route needs a logged-in user.
# Ownership (only the pharmacy's owner can create/edit its branches) is
# checked per-route below -- same pattern as the pharmacy router, and the
# same TODO applies once Staff/Role exists: this should become a
# permission check (e.g. "staff_management" or a branch-scoped role)
# instead of a raw owner-id comparison.
router = APIRouter(tags=["branch"])


def _get_branch_and_assert_owner(db: DbSession, branch_id: str, user_id: str):
    branch = service.get_branch_or_404(db, branch_id)
    pharmacy = pharmacy_service.get_pharmacy_or_404(db, branch.pharmacy_id)
    pharmacy_service.assert_is_owner(db, pharmacy, user_id)
    return branch


@router.post(
    "/pharmacies/{pharmacy_id}/branches",
    response_model=BranchRead,
    status_code=201,
    summary="Create a new branch",
    description="Create a new branch under a specific pharmacy profile. Requires owner authorization.",
    responses={
        400: {"description": "Invalid input"},
        401: {"description": "Authentication required"},
        403: {"description": "Not authorized to create a branch under this pharmacy"},
        404: {"description": "Pharmacy not found"},
        409: {"description": "Branch with this name already exists for this pharmacy"},
        422: {"description": "Validation error"},
    },
)
def create_branch(
    pharmacy_id: str,
    payload: BranchCreate,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    pharmacy = pharmacy_service.get_pharmacy_or_404(db, pharmacy_id)
    pharmacy_service.assert_is_owner(db, pharmacy, current_user.id)
    return service.create_branch(db, pharmacy_id, payload)


@router.get(
    "/pharmacies/{pharmacy_id}/branches",
    response_model=list[BranchRead],
    summary="List branches for a pharmacy",
    description="Retrieve branches belonging to a specific pharmacy with optional status filtering and pagination. Only authorized owners can view.",
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Not authorized to view branches of this pharmacy"},
        404: {"description": "Pharmacy not found"},
    },
)
def list_branches(
    pharmacy_id: str,
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    include_inactive: bool = False,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    pharmacy = pharmacy_service.get_pharmacy_or_404(db, pharmacy_id)
    pharmacy_service.assert_is_owner(db, pharmacy, current_user.id)
    return service.list_branches_for_pharmacy(
        db,
        pharmacy_id,
        skip=skip,
        limit=limit,
        status=status,
        include_inactive=include_inactive,
    )


@router.get(
    "/branches/{branch_id}",
    response_model=BranchRead,
    summary="Get branch by ID",
    description="Retrieve detailed information for a specific branch. Only authorized owners can view.",
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Not authorized to access this branch"},
        404: {"description": "Branch not found"},
    },
)
def read_branch(
    branch_id: str,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    return _get_branch_and_assert_owner(db, branch_id, current_user.id)


@router.patch(
    "/branches/{branch_id}",
    response_model=BranchRead,
    summary="Update branch details",
    description="Update non-null attributes of a specific branch. Requires owner authorization.",
    responses={
        400: {"description": "Invalid input"},
        401: {"description": "Authentication required"},
        403: {"description": "Not authorized to modify this branch"},
        404: {"description": "Branch not found"},
        409: {"description": "Branch with this name already exists for this pharmacy"},
        422: {"description": "Validation error"},
    },
)
def update_branch(
    branch_id: str,
    payload: BranchUpdate,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    branch = _get_branch_and_assert_owner(db, branch_id, current_user.id)
    return service.update_branch(db, branch, payload)


@router.patch(
    "/branches/{branch_id}/status",
    response_model=BranchRead,
    summary="Update branch operational status",
    description="Transition branch status between active and inactive, synchronizing the is_active flag.",
    responses={
        400: {"description": "Invalid input status"},
        401: {"description": "Authentication required"},
        403: {"description": "Not authorized to modify this branch"},
        404: {"description": "Branch not found"},
        422: {"description": "Validation error"},
    },
)
def update_branch_status(
    branch_id: str,
    payload: BranchStatusUpdate,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    branch = _get_branch_and_assert_owner(db, branch_id, current_user.id)
    return service.update_branch_status(db, branch, payload.status)


@router.delete(
    "/branches/{branch_id}",
    status_code=204,
    summary="Soft delete a branch",
    description="Deactivate and soft delete a branch by ID. Requires owner authorization.",
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Not authorized to delete this branch"},
        404: {"description": "Branch not found"},
    },
)
def delete_branch(
    branch_id: str,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    branch = _get_branch_and_assert_owner(db, branch_id, current_user.id)
    service.delete_branch(db, branch)
