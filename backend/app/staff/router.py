"""
app/staff/router.py

FastAPI router endpoints for Staff Management, Roles, Permissions, and Attendance.
Enforces strict RBAC via `assert_has_permission` and maintains branch/pharmacy isolation.
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status, Request, Response
from sqlalchemy.orm import Session as DbSession, joinedload

from app.db.base import get_db
from app.pharmacy.models import PharmacyOwner
from app.shared.rate_limit import limiter
from app.licensing.deps import get_current_licensed_user
from app.staff import service
from app.staff.models import AttendanceRecord, Permission, StaffMember, StaffRole
from app.staff.permissions import Permissions
from app.staff.schemas import (
    AttendanceCheckIn,
    AttendanceCheckOut,
    AttendanceOverride,
    AttendanceRead,
    PermissionRead,
    StaffMemberCreate,
    StaffMemberRead,
    StaffMemberStatusUpdate,
    StaffMemberUpdate,
    StaffRoleCreate,
    StaffRoleRead,
    StaffRoleUpdate,
)
from app.user.models import User

router = APIRouter(tags=["staff"])


@router.get(
    "/pharmacies/{pharmacy_id}/permissions",
    response_model=list[PermissionRead],
    summary="List all system permissions",
    description="Retrieve all granular permissions available for role assignments.",
)
def list_permissions(
    pharmacy_id: str,
    response: Response,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    service.assert_has_permission(db, current_user.id, pharmacy_id, Permissions.STAFF_READ.code, response=response)
    return db.query(Permission).order_by(Permission.category, Permission.code).all()


@router.get(
    "/pharmacies/{pharmacy_id}/roles",
    response_model=list[StaffRoleRead],
    summary="List system and custom roles",
    description="Retrieve all immutable system roles plus custom roles created for this pharmacy.",
)
def list_roles(
    pharmacy_id: str,
    response: Response,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    service.assert_has_permission(db, current_user.id, pharmacy_id, Permissions.STAFF_READ.code, response=response)
    return (
        db.query(StaffRole)
        .options(joinedload(StaffRole.permissions))
        .filter((StaffRole.pharmacy_id == pharmacy_id) | (StaffRole.pharmacy_id.is_(None)))
        .order_by(StaffRole.level.desc(), StaffRole.name)
        .all()
    )


@router.post(
    "/pharmacies/{pharmacy_id}/roles",
    response_model=StaffRoleRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a custom staff role",
    description="Create a new custom role scoped to this pharmacy with specified permission codes.",
)
@limiter.limit("20/minute")
def create_role(
    request: Request,
    pharmacy_id: str,
    payload: StaffRoleCreate,
    response: Response,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    actor_staff = service.assert_has_permission(db, current_user.id, pharmacy_id, Permissions.ROLE_MANAGE.code, response=response)
    return service.create_role(db, pharmacy_id, payload, current_user.id, actor_staff=actor_staff)


@router.patch(
    "/pharmacies/{pharmacy_id}/roles/{role_id}",
    response_model=StaffRoleRead,
    summary="Update a custom staff role",
    description="Update non-null attributes or permission codes of a custom role scoped to this pharmacy.",
)
@limiter.limit("20/minute")
def update_role(
    request: Request,
    pharmacy_id: str,
    role_id: str,
    payload: StaffRoleUpdate,
    response: Response,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    actor_staff = service.assert_has_permission(db, current_user.id, pharmacy_id, Permissions.ROLE_MANAGE.code, response=response)
    return service.update_role(db, pharmacy_id, role_id, payload, current_user.id, actor_staff=actor_staff)


@router.delete(
    "/pharmacies/{pharmacy_id}/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a custom staff role",
    description="Delete a custom role scoped to this pharmacy. Fails if the role is assigned to any staff member.",
)
@limiter.limit("20/minute")
def delete_role(
    request: Request,
    pharmacy_id: str,
    role_id: str,
    response: Response,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    service.assert_has_permission(db, current_user.id, pharmacy_id, Permissions.ROLE_MANAGE.code, response=response)
    service.delete_role(db, pharmacy_id, role_id, current_user.id)


@router.get(
    "/pharmacies/{pharmacy_id}/staff",
    response_model=list[StaffMemberRead],
    summary="List staff members",
    description="Retrieve staff members belonging to a pharmacy with optional branch and status filtering.",
)
def list_staff(
    pharmacy_id: str,
    response: Response,
    branch_id: str | None = Query(None, description="Filter by branch UUID"),
    status_filter: str | None = Query(None, alias="status", description="Filter by status ('active', 'disabled', 'terminated')"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    # Enforce horizontal branch isolation: if filtering by branch_id, check permissions for that branch
    service.assert_has_permission(db, current_user.id, pharmacy_id, Permissions.STAFF_READ.code, target_branch_id=branch_id, response=response)

    query = (
        db.query(StaffMember)
        .options(joinedload(StaffMember.role).joinedload(StaffRole.permissions))
        .filter(StaffMember.pharmacy_id == pharmacy_id)
    )
    if branch_id:
        query = query.filter(StaffMember.branch_id == branch_id)
    if status_filter:
        query = query.filter(StaffMember.status == status_filter)

    return query.order_by(StaffMember.created_at.desc()).offset(skip).limit(limit).all()


@router.post(
    "/pharmacies/{pharmacy_id}/staff",
    response_model=StaffMemberRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new staff member",
    description="Assign a new employee to a branch and role within this pharmacy.",
)
@limiter.limit("20/minute")
def create_staff(
    request: Request,
    pharmacy_id: str,
    payload: StaffMemberCreate,
    response: Response,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    actor_staff = service.assert_has_permission(
        db, current_user.id, pharmacy_id, Permissions.STAFF_MANAGE.code, target_branch_id=payload.branch_id, response=response
    )
    return service.create_staff_member(db, pharmacy_id, payload, current_user.id, actor_staff=actor_staff)


@router.get(
    "/pharmacies/{pharmacy_id}/staff/{staff_id}",
    response_model=StaffMemberRead,
    summary="Get staff member details",
    description="Retrieve detailed profile and role information for a specific staff member.",
)
def get_staff(
    pharmacy_id: str,
    staff_id: str,
    response: Response,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    staff = service.get_staff_or_404(db, staff_id, pharmacy_id)
    service.assert_has_permission(db, current_user.id, pharmacy_id, Permissions.STAFF_READ.code, target_branch_id=staff.branch_id, response=response)
    return staff


@router.patch(
    "/pharmacies/{pharmacy_id}/staff/{staff_id}",
    response_model=StaffMemberRead,
    summary="Update staff member profile",
    description="Modify non-null attributes, branch assignment, or role of a staff member.",
)
def update_staff(
    pharmacy_id: str,
    staff_id: str,
    payload: StaffMemberUpdate,
    response: Response,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    staff = service.get_staff_or_404(db, staff_id, pharmacy_id)
    actor_staff = service.assert_has_permission(
        db, current_user.id, pharmacy_id, Permissions.STAFF_MANAGE.code, target_branch_id=staff.branch_id, response=response
    )
    return service.update_staff_member(db, staff, payload, current_user.id, actor_staff=actor_staff)


@router.patch(
    "/pharmacies/{pharmacy_id}/staff/{staff_id}/status",
    response_model=StaffMemberRead,
    summary="Update staff employment status",
    description="Transition employee status between 'active', 'disabled', and 'terminated', revoking active sessions if disabled/terminated.",
)
def update_staff_status(
    pharmacy_id: str,
    staff_id: str,
    payload: StaffMemberStatusUpdate,
    response: Response,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    staff = service.get_staff_or_404(db, staff_id, pharmacy_id)
    service.assert_has_permission(db, current_user.id, pharmacy_id, Permissions.STAFF_MANAGE.code, target_branch_id=staff.branch_id, response=response)
    return service.set_staff_status(db, staff, payload.status, current_user.id)


def _assert_can_record_attendance(db: DbSession, current_user: User, pharmacy_id: str, staff: StaffMember, response: Response | None = None) -> None:
    """Helper allowing either the staff member themselves (if active) or a supervisor with attendance:write to record check in/out."""
    if staff.user_id == current_user.id and staff.status == "active":
        return  # Self check-in / check-out
    service.assert_has_permission(db, current_user.id, pharmacy_id, Permissions.ATTENDANCE_CHECKIN.code, target_branch_id=staff.branch_id, response=response)


@router.post(
    "/pharmacies/{pharmacy_id}/staff/{staff_id}/check-in",
    response_model=AttendanceRead,
    status_code=status.HTTP_201_CREATED,
    summary="Record attendance check-in",
    description="Start a working shift for a staff member. Prevents double check-ins.",
)
@limiter.limit("20/minute")
def check_in_staff(
    request: Request,
    pharmacy_id: str,
    staff_id: str,
    payload: AttendanceCheckIn,
    response: Response,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    staff = service.get_staff_or_404(db, staff_id, pharmacy_id)
    _assert_can_record_attendance(db, current_user, pharmacy_id, staff, response=response)
    return service.check_in(db, staff, current_user.id, payload.notes)


@router.post(
    "/pharmacies/{pharmacy_id}/staff/{staff_id}/check-out",
    response_model=AttendanceRead,
    summary="Record attendance check-out",
    description="End the active working shift for a staff member and compute total working minutes.",
)
@limiter.limit("20/minute")
def check_out_staff(
    request: Request,
    pharmacy_id: str,
    staff_id: str,
    payload: AttendanceCheckOut,
    response: Response,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    staff = service.get_staff_or_404(db, staff_id, pharmacy_id)
    _assert_can_record_attendance(db, current_user, pharmacy_id, staff, response=response)
    return service.check_out(db, staff, current_user.id, payload.notes)


@router.patch(
    "/pharmacies/{pharmacy_id}/attendance/{attendance_id}/override",
    response_model=AttendanceRead,
    summary="Supervisor manual attendance check-out override",
    description="Manually correct or close an abandoned shift check-out timestamp with mandatory justification.",
)
@limiter.limit("20/minute")
def override_attendance(
    request: Request,
    pharmacy_id: str,
    attendance_id: str,
    payload: AttendanceOverride,
    response: Response,
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    record = db.query(AttendanceRecord).filter(
        AttendanceRecord.id == attendance_id,
        AttendanceRecord.pharmacy_id == pharmacy_id
    ).first()
    if not record:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Attendance record not found")
    actor_staff = service.assert_has_permission(db, current_user.id, pharmacy_id, Permissions.ATTENDANCE_OVERRIDE.code, target_branch_id=record.branch_id, response=response)
    return service.override_check_out(db, attendance_id, pharmacy_id, payload, current_user.id, actor_staff=actor_staff)


@router.get(
    "/pharmacies/{pharmacy_id}/attendance",
    response_model=list[AttendanceRead],
    summary="List attendance logs",
    description="Retrieve historical check-in and check-out records with optional date range and staff filtering.",
)
def list_attendance(
    pharmacy_id: str,
    response: Response,
    branch_id: str | None = Query(None, description="Filter by branch UUID"),
    staff_id: str | None = Query(None, description="Filter by staff UUID"),
    from_date: datetime | None = Query(None, description="Start date filter (UTC)"),
    to_date: datetime | None = Query(None, description="End date filter (UTC)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(get_current_licensed_user),
    db: DbSession = Depends(get_db),
):
    service.assert_has_permission(db, current_user.id, pharmacy_id, Permissions.ATTENDANCE_READ.code, target_branch_id=branch_id, response=response)

    query = db.query(AttendanceRecord).filter(AttendanceRecord.pharmacy_id == pharmacy_id)
    if branch_id:
        query = query.filter(AttendanceRecord.branch_id == branch_id)
    if staff_id:
        query = query.filter(AttendanceRecord.staff_id == staff_id)
    if from_date:
        query = query.filter(AttendanceRecord.check_in_at >= from_date)
    if to_date:
        query = query.filter(AttendanceRecord.check_in_at <= to_date)

    return query.order_by(AttendanceRecord.check_in_at.desc()).offset(skip).limit(limit).all()
