"""
app/staff/service.py

Service layer containing core business logic for Staff Management, Roles, Permissions, and Attendance.
Enforces strict pharmacy/branch isolation, double check-in prevention, vertical/horizontal authorization,
and immediate session revocation upon staff deactivation.
"""

from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as DbSession, joinedload
from fastapi import HTTPException, status, Response

from app.auth.models import Session as AuthSession
from app.branch.models import Branch
from app.core.config import settings
from app.pharmacy.models import PharmacyOwner
from app.services.audit import audit_log
from app.staff.models import AttendanceRecord, Permission, StaffMember, StaffRole
from app.staff.permissions import SYSTEM_ROLES_CONFIG, Permissions
from app.staff.schemas import AttendanceOverride, StaffMemberCreate, StaffMemberUpdate, StaffRoleCreate, StaffRoleUpdate


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def seed_system_roles_and_permissions(db: DbSession) -> None:
    """
    Idempotent seeding of standard system permissions and immutable system roles.
    Called on app initialization or migration.
    """
    # 1. Seed Permissions
    perm_map = {}

    # Seeding granular permissions
    for p_def in Permissions.all_definitions():
        perm = db.query(Permission).filter(Permission.code == p_def.code).first()
        if not perm:
            perm = Permission(code=p_def.code, category=p_def.category, description=p_def.description)
            db.add(perm)
            db.flush()
        perm_map[p_def.code] = perm

    # 2. Seed System Roles
    for role_cfg in SYSTEM_ROLES_CONFIG:
        role_name = role_cfg["name"]
        role = db.query(StaffRole).filter(StaffRole.name == role_name, StaffRole.pharmacy_id.is_(None)).first()
        if not role:
            role = StaffRole(
                pharmacy_id=None,
                name=role_name,
                description=role_cfg["description"],
                is_system=True,
                level=role_cfg["level"],
            )
            db.add(role)
            db.flush()
        else:
            role.level = role_cfg["level"]
            role.description = role_cfg["description"]

        # Sync permissions
        assigned_codes = set(role_cfg["permissions"])
        role.permissions = [perm_map[c] for c in assigned_codes if c in perm_map]

    db.commit()


def get_staff_role_or_404(db: DbSession, role_id: str, pharmacy_id: str) -> StaffRole:
    role = (
        db.query(StaffRole)
        .filter(StaffRole.id == role_id, (StaffRole.pharmacy_id == pharmacy_id) | (StaffRole.pharmacy_id.is_(None)))
        .first()
    )
    if not role:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Role not found")
    return role


def assert_has_permission(
    db: DbSession,
    user_id: str,
    pharmacy_id: str,
    required_permission_code: str,
    target_branch_id: str | None = None,
    response: Response | None = None,
) -> StaffMember | None:
    """
    Check if the authenticated user has the required permission within the pharmacy.
    Returns None if the user is a PharmacyOwner (super-admin), or the StaffMember object if granted by role.
    Raises HTTP 403 if access is denied.
    """
    # 1. Check direct ownership
    is_owner = (
        db.query(PharmacyOwner.pharmacy_id)
        .filter(PharmacyOwner.pharmacy_id == pharmacy_id, PharmacyOwner.user_id == user_id)
        .first()
    )
    if is_owner:
        return None  # PharmacyOwner has full authorization across all branches

    # 2. Query active staff assignment with eager loaded role and permissions
    staff = (
        db.query(StaffMember)
        .options(joinedload(StaffMember.role).joinedload(StaffRole.permissions))
        .filter(
            StaffMember.user_id == user_id,
            StaffMember.pharmacy_id == pharmacy_id,
            StaffMember.status == "active",
        )
        .first()
    )
    if not staff or not staff.role:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Access denied: you are not an active staff member or owner of this pharmacy",
        )

    # 3. Horizontal branch check: If target_branch_id is requested, ensure staff is assigned to that branch
    # unless their role is an Owner or Admin system role which spans across all branches of the pharmacy.
    if target_branch_id and staff.role.name not in ("Owner", "Admin"):
        if staff.branch_id != target_branch_id:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Access denied: your role is restricted to your assigned branch",
            )

    # 4. Check system super-admin roles or permission list
    if staff.role.name in ("Owner", "Admin"):
        return staff

    user_permissions = {p.code for p in staff.role.permissions}
    if required_permission_code not in user_permissions:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"Access denied: missing required permission '{required_permission_code}'",
        )

    return staff


def get_current_pharmacy_id(
    db: DbSession,
    user_id: str,
    pharmacy_id: str | None = None,
    required_permission_code: str | None = None,
) -> str:
    """
    Resolve the active pharmacy ID for the user and optionally verify permission.
    If pharmacy_id is not passed, automatically finds the user's pharmacy (as owner or active staff).
    """
    if not pharmacy_id:
        owner_entry = db.query(PharmacyOwner).filter(PharmacyOwner.user_id == user_id).first()
        if owner_entry:
            pharmacy_id = owner_entry.pharmacy_id
        else:
            staff_entry = (
                db.query(StaffMember)
                .filter(StaffMember.user_id == user_id, StaffMember.status == "active")
                .first()
            )
            if staff_entry:
                pharmacy_id = staff_entry.pharmacy_id
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: user is not associated with any active pharmacy",
                )

    if required_permission_code:
        assert_has_permission(db, user_id, pharmacy_id, required_permission_code)

    return pharmacy_id


def _assert_vertical_role_tier(actor_staff: StaffMember | None, target_role: StaffRole) -> None:
    """Ensure an actor cannot assign or modify a role whose tier (level) exceeds their own."""
    if actor_staff is None:
        return  # Actor is PharmacyOwner, full access
    if actor_staff.role:
        if target_role.level > actor_staff.role.level:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Cannot assign or manage a role higher than your own privilege level",
            )
        if actor_staff.role.level == 80 and target_role.level > 50:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Cannot assign or manage a role higher than your own privilege level: Managers can only assign roles up to level 50",
            )
        if actor_staff.role.level < 100 and target_role.level >= actor_staff.role.level:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Cannot assign or manage a role equal to or higher than your own privilege level",
            )


def _check_staff_uniqueness(
    db: DbSession,
    pharmacy_id: str,
    email: str | None,
    phone: str | None,
    user_id: str | None,
    ignore_staff_id: str | None = None,
) -> None:
    if email:
        query = db.query(StaffMember.id).filter(StaffMember.pharmacy_id == pharmacy_id, StaffMember.contact_email == email)
        if ignore_staff_id:
            query = query.filter(StaffMember.id != ignore_staff_id)
        if query.first():
            raise HTTPException(status.HTTP_409_CONFLICT, "A staff member with this email already exists in this pharmacy")

    if phone:
        query = db.query(StaffMember.id).filter(StaffMember.pharmacy_id == pharmacy_id, StaffMember.contact_phone == phone)
        if ignore_staff_id:
            query = query.filter(StaffMember.id != ignore_staff_id)
        if query.first():
            raise HTTPException(status.HTTP_409_CONFLICT, "A staff member with this phone already exists in this pharmacy")

    if user_id:
        query = db.query(StaffMember.id).filter(StaffMember.pharmacy_id == pharmacy_id, StaffMember.user_id == user_id)
        if ignore_staff_id:
            query = query.filter(StaffMember.id != ignore_staff_id)
        if query.first():
            raise HTTPException(status.HTTP_409_CONFLICT, "This user account is already assigned as a staff member in this pharmacy")


def create_role(
    db: DbSession,
    pharmacy_id: str,
    payload: StaffRoleCreate,
    actor_user_id: str,
    actor_staff: StaffMember | None = None,
) -> StaffRole:
    existing = (
        db.query(StaffRole.id)
        .filter(StaffRole.pharmacy_id == pharmacy_id, StaffRole.name == payload.name)
        .first()
    )
    if existing:
        raise HTTPException(status.HTTP_409_CONFLICT, "A custom role with this name already exists for this pharmacy")

    perms = db.query(Permission).filter(Permission.code.in_(payload.permissions)).all()
    if len(perms) != len(set(payload.permissions)):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "One or more invalid permission codes provided")

    # Privilege containment gate: non-owner actor can only assign permissions they hold explicitly
    if actor_staff and actor_staff.role and actor_staff.role.level < 100:
        actor_effective_perms = {p.code for p in actor_staff.role.permissions}
        for req_perm in payload.permissions:
            if req_perm not in actor_effective_perms:
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN,
                    f"Cannot assign permission '{req_perm}' which you do not possess",
                )

    role = StaffRole(
        pharmacy_id=pharmacy_id,
        name=payload.name,
        description=payload.description,
        is_system=False,
        level=10,  # Custom roles default to level 10
        permissions=perms,
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    audit_log("ROLE_CREATED", pharmacy_id=pharmacy_id, role_id=role.id, role_name=role.name, actor_user_id=actor_user_id)
    return role


def update_role(
    db: DbSession,
    pharmacy_id: str,
    role_id: str,
    payload: StaffRoleUpdate,
    actor_user_id: str,
    actor_staff: StaffMember | None = None,
) -> StaffRole:
    role = db.query(StaffRole).filter(StaffRole.id == role_id).first()
    if not role:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Role not found")
    
    # Verify role.is_system is False and role.pharmacy_id == actor.pharmacy_id (custom role lifecycle security)
    if role.is_system or role.pharmacy_id != pharmacy_id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Cannot modify system roles or roles belonging to another pharmacy",
        )
    
    updates = payload.model_dump(exclude_unset=True)
    
    if "name" in updates:
        # Verify name is unique within the pharmacy
        existing = (
            db.query(StaffRole.id)
            .filter(StaffRole.pharmacy_id == pharmacy_id, StaffRole.name == updates["name"], StaffRole.id != role_id)
            .first()
        )
        if existing:
            raise HTTPException(status.HTTP_409_CONFLICT, "A custom role with this name already exists for this pharmacy")
        role.name = updates["name"]
        
    if "description" in updates:
        role.description = updates["description"]
        
    if "permissions" in updates and updates["permissions"] is not None:
        perms = db.query(Permission).filter(Permission.code.in_(updates["permissions"])).all()
        if len(perms) != len(set(updates["permissions"])):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "One or more invalid permission codes provided")
        
        # Privilege containment gate: non-owner actor can only assign permissions they hold explicitly
        if actor_staff and actor_staff.role and actor_staff.role.level < 100:
            actor_effective_perms = {p.code for p in actor_staff.role.permissions}
            for req_perm in updates["permissions"]:
                if req_perm not in actor_effective_perms:
                    raise HTTPException(
                        status.HTTP_403_FORBIDDEN,
                        f"Cannot assign permission '{req_perm}' which you do not possess",
                    )
        role.permissions = perms
        
    db.commit()
    db.refresh(role)
    audit_log("ROLE_UPDATED", pharmacy_id=pharmacy_id, role_id=role.id, role_name=role.name, actor_user_id=actor_user_id)
    return role


def delete_role(
    db: DbSession,
    pharmacy_id: str,
    role_id: str,
    actor_user_id: str,
) -> None:
    role = db.query(StaffRole).filter(StaffRole.id == role_id).first()
    if not role:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Role not found")
    
    # Verify role.is_system is False and role.pharmacy_id == actor.pharmacy_id (custom role lifecycle security)
    if role.is_system or role.pharmacy_id != pharmacy_id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Cannot delete system roles or roles belonging to another pharmacy",
        )
    
    # Prevent deleting if assigned to active staff
    assigned_staff = db.query(StaffMember.id).filter(StaffMember.role_id == role_id).first()
    if assigned_staff:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Cannot delete role because it is currently assigned to one or more staff members",
        )
        
    db.delete(role)
    db.commit()
    audit_log("ROLE_DELETED", pharmacy_id=pharmacy_id, role_id=role_id, role_name=role.name, actor_user_id=actor_user_id)


def get_staff_or_404(db: DbSession, staff_id: str, pharmacy_id: str) -> StaffMember:
    staff = (
        db.query(StaffMember)
        .options(joinedload(StaffMember.role).joinedload(StaffRole.permissions))
        .filter(StaffMember.id == staff_id, StaffMember.pharmacy_id == pharmacy_id)
        .first()
    )
    if not staff:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Staff member not found")
    return staff


def create_staff_member(
    db: DbSession,
    pharmacy_id: str,
    payload: StaffMemberCreate,
    actor_user_id: str,
    actor_staff: StaffMember | None = None,
) -> StaffMember:
    # 1. Verify branch exists and belongs to pharmacy
    branch = db.query(Branch.id).filter(Branch.id == payload.branch_id, Branch.pharmacy_id == pharmacy_id, Branch.is_active == True).first()
    if not branch:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid or inactive branch specified for this pharmacy")

    # 2. Verify role exists and check vertical privilege
    role = get_staff_role_or_404(db, payload.role_id, pharmacy_id)
    _assert_vertical_role_tier(actor_staff, role)

    # 3. Check uniqueness of email, phone, and user_id within pharmacy
    _check_staff_uniqueness(db, pharmacy_id, payload.contact_email, payload.contact_phone, payload.user_id)

    staff = StaffMember(
        pharmacy_id=pharmacy_id,
        branch_id=payload.branch_id,
        role_id=payload.role_id,
        user_id=payload.user_id,
        employee_code=payload.employee_code,
        first_name=payload.first_name,
        last_name=payload.last_name,
        contact_phone=payload.contact_phone,
        contact_email=payload.contact_email,
        status="active",
    )
    db.add(staff)
    db.commit()
    db.refresh(staff)
    audit_log(
        "EMPLOYEE_ADDED",
        pharmacy_id=pharmacy_id,
        branch_id=staff.branch_id,
        staff_id=staff.id,
        role_id=staff.role_id,
        actor_user_id=actor_user_id,
    )
    return staff


def update_staff_member(
    db: DbSession,
    staff: StaffMember,
    payload: StaffMemberUpdate,
    actor_user_id: str,
    actor_staff: StaffMember | None = None,
) -> StaffMember:
    updates = payload.model_dump(exclude_unset=True)

    # Self-management check: employees cannot modify their own role or branch assignment
    if actor_staff and actor_staff.id == staff.id:
        if "role_id" in updates or "branch_id" in updates:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Cannot modify your own role or branch assignment")

    if "branch_id" in updates and updates["branch_id"]:
        branch = db.query(Branch.id).filter(Branch.id == updates["branch_id"], Branch.pharmacy_id == staff.pharmacy_id, Branch.is_active == True).first()
        if not branch:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid or inactive branch specified for this pharmacy")

    if "role_id" in updates and updates["role_id"]:
        role = get_staff_role_or_404(db, updates["role_id"], staff.pharmacy_id)
        _assert_vertical_role_tier(actor_staff, role)

    _check_staff_uniqueness(
        db,
        staff.pharmacy_id,
        updates.get("contact_email", staff.contact_email),
        updates.get("contact_phone", staff.contact_phone),
        updates.get("user_id", staff.user_id),
        ignore_staff_id=staff.id,
    )

    old_role_id = staff.role_id
    for k, v in updates.items():
        setattr(staff, k, v)

    db.commit()
    db.refresh(staff)

    if old_role_id != staff.role_id:
        audit_log("ROLE_ASSIGNED", pharmacy_id=staff.pharmacy_id, staff_id=staff.id, old_role_id=old_role_id, new_role_id=staff.role_id, actor_user_id=actor_user_id)
    else:
        audit_log("EMPLOYEE_UPDATED", pharmacy_id=staff.pharmacy_id, staff_id=staff.id, updated_fields=list(updates.keys()), actor_user_id=actor_user_id)

    return staff


def set_staff_status(
    db: DbSession,
    staff: StaffMember,
    new_status: str,
    actor_user_id: str,
) -> StaffMember:
    if staff.user_id == actor_user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Cannot disable or terminate your own employment account")

    old_status = staff.status
    staff.status = new_status

    # Security check: If disabled or terminated, immediately revoke all active sessions for the linked user
    if new_status in ("disabled", "terminated") and staff.user_id:
        from app.auth.service import revoke_sessions
        revoke_sessions(
            db,
            db.query(AuthSession).filter(AuthSession.user_id == staff.user_id),
            logout_reason="admin_revoked",
        )

    db.commit()
    db.refresh(staff)

    audit_log(
        f"EMPLOYEE_{new_status.upper()}",
        pharmacy_id=staff.pharmacy_id,
        staff_id=staff.id,
        old_status=old_status,
        new_status=new_status,
        actor_user_id=actor_user_id,
    )
    return staff


def check_in(
    db: DbSession,
    staff: StaffMember,
    actor_user_id: str,
    notes: str | None = None,
) -> AttendanceRecord:
    if staff.status != "active":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Cannot record attendance for inactive or terminated staff members")

    # Check for existing active check-in
    active = db.query(AttendanceRecord).filter(AttendanceRecord.staff_id == staff.id, AttendanceRecord.check_out_at.is_(None)).first()
    if active:
        raise HTTPException(status.HTTP_409_CONFLICT, "Employee is already checked in. Must check out before checking in again.")

    record = AttendanceRecord(
        pharmacy_id=staff.pharmacy_id,
        branch_id=staff.branch_id,
        staff_id=staff.id,
        check_in_at=_utcnow(),
        notes=notes,
    )
    db.add(record)
    try:
        db.commit()
        db.refresh(record)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Employee is already checked in. Must check out before checking in again.")

    audit_log("ATTENDANCE_CHECK_IN", pharmacy_id=staff.pharmacy_id, branch_id=staff.branch_id, staff_id=staff.id, attendance_id=record.id, actor_user_id=actor_user_id)
    return record


def check_out(
    db: DbSession,
    staff: StaffMember,
    actor_user_id: str,
    notes: str | None = None,
) -> AttendanceRecord:
    record = db.query(AttendanceRecord).filter(AttendanceRecord.staff_id == staff.id, AttendanceRecord.check_out_at.is_(None)).first()
    if not record:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No active check-in found for this employee.")

    record.check_out_at = _utcnow()
    # Calculate duration in minutes
    delta = record.check_out_at - record.check_in_at
    record.working_minutes = int(delta.total_seconds() / 60)
    if notes:
        record.notes = f"{record.notes or ''} | Out: {notes}".strip(" |")

    db.commit()
    db.refresh(record)
    audit_log("ATTENDANCE_CHECK_OUT", pharmacy_id=staff.pharmacy_id, branch_id=staff.branch_id, staff_id=staff.id, attendance_id=record.id, working_minutes=record.working_minutes, actor_user_id=actor_user_id)
    return record


def override_check_out(
    db: DbSession,
    attendance_id: str,
    pharmacy_id: str,
    payload: AttendanceOverride,
    actor_user_id: str,
    actor_staff: StaffMember | None = None,
) -> AttendanceRecord:
    record = db.query(AttendanceRecord).filter(AttendanceRecord.id == attendance_id, AttendanceRecord.pharmacy_id == pharmacy_id).first()
    if not record:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Attendance record not found")

    # Segregation of Duties (SoD): staff cannot override their own check-out unless L100 Owner
    if actor_staff and record.staff_id == actor_staff.id and (not actor_staff.role or actor_staff.role.level < 100):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Segregation of Duties violation: cannot perform check-out override on your own attendance record",
        )

    new_out = payload.new_check_out_at

    if new_out <= record.check_in_at:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "new_check_out_at must be later than check_in_at")

    record.check_out_at = new_out
    delta = record.check_out_at - record.check_in_at
    record.working_minutes = int(delta.total_seconds() / 60)
    record.notes = f"{record.notes or ''} [Supervisor Override: {payload.override_reason}]".strip()

    db.commit()
    db.refresh(record)
    audit_log("ATTENDANCE_OVERRIDE", pharmacy_id=pharmacy_id, attendance_id=record.id, staff_id=record.staff_id, actor_user_id=actor_user_id, override_reason=payload.override_reason)
    return record
