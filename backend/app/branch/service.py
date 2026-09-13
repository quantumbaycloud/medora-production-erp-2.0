from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.branch.models import Branch, BRANCH_STATUSES
from app.branch.schemas import BranchCreate, BranchUpdate
from app.services.audit import audit_log


def _check_duplicate_branch_name(
    db: Session, pharmacy_id: str, name: str | None, ignore_branch_id: str | None = None
) -> None:
    if not name:
        return
    name = name.strip()
    query = db.query(Branch.id).filter(
        Branch.pharmacy_id == pharmacy_id,
        Branch.name == name,
        Branch.is_active == True,
    )
    if ignore_branch_id:
        query = query.filter(Branch.id != ignore_branch_id)
    if query.first():
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "An active branch with this name already exists for this pharmacy",
        )


def create_branch(db: Session, pharmacy_id: str, payload: BranchCreate) -> Branch:
    _check_duplicate_branch_name(db, pharmacy_id, payload.name)
    branch = Branch(pharmacy_id=pharmacy_id, status="active", is_active=True, **payload.model_dump())
    db.add(branch)
    db.commit()
    db.refresh(branch)
    audit_log("BRANCH_CREATED", pharmacy_id=pharmacy_id, branch_id=branch.id, branch_name=branch.name)
    return branch


def get_branch(db: Session, branch_id: str) -> Branch | None:
    return db.query(Branch).filter(Branch.id == branch_id).first()


def get_branch_or_404(db: Session, branch_id: str) -> Branch:
    branch = get_branch(db, branch_id)
    if not branch:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Branch not found")
    return branch


def list_branches_for_pharmacy(
    db: Session,
    pharmacy_id: str,
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    include_inactive: bool = False,
) -> list[Branch]:
    query = db.query(Branch).filter(Branch.pharmacy_id == pharmacy_id)
    if not include_inactive:
        query = query.filter(Branch.is_active == True)
    if status is not None:
        query = query.filter(Branch.status == status)
    return query.offset(skip).limit(limit).all()


def update_branch(db: Session, branch: Branch, payload: BranchUpdate) -> Branch:
    updates = payload.model_dump(exclude_unset=True)
    if "name" in updates and updates["name"]:
        _check_duplicate_branch_name(db, branch.pharmacy_id, updates["name"], ignore_branch_id=branch.id)
    for field, value in updates.items():
        setattr(branch, field, value)
    db.commit()
    db.refresh(branch)
    audit_log("BRANCH_UPDATED", branch_id=branch.id, updated_fields=list(updates.keys()))
    return branch


def update_branch_status(db: Session, branch: Branch, new_status: str) -> Branch:
    if new_status not in BRANCH_STATUSES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"status must be one of {BRANCH_STATUSES}")
    branch.status = new_status
    branch.is_active = (new_status != "inactive")
    db.commit()
    db.refresh(branch)
    audit_log("BRANCH_STATUS_UPDATED", branch_id=branch.id, status=new_status, is_active=branch.is_active)
    return branch


def delete_branch(db: Session, branch: Branch) -> None:
    branch.status = "inactive"
    branch.is_active = False
    db.commit()
    audit_log("BRANCH_SOFT_DELETED", branch_id=branch.id, pharmacy_id=branch.pharmacy_id)
