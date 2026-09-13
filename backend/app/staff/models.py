"""
app/staff/models.py

SQLAlchemy ORM models for Staff Management, Roles, Permissions, and Attendance.
Strictly respects module isolation and integrates into the existing dependency chain:
Auth -> User -> Pharmacy -> Branch -> Staff.
"""

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base, new_uuid

STAFF_STATUSES = ("active", "disabled", "terminated")


class StaffRole(Base):
    __tablename__ = "staff_roles"

    id = Column(String, primary_key=True, default=new_uuid)
    # If pharmacy_id is None, it is a global/system role shared across all pharmacies.
    pharmacy_id = Column(String, ForeignKey("pharmacies.id", ondelete="CASCADE"), nullable=True, index=True)

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_system = Column(Boolean, default=False, nullable=False)
    # Tier/level used for vertical privilege checks (higher level cannot be assigned by lower level).
    level = Column(Integer, default=10, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # ORM Relationships
    pharmacy = relationship("Pharmacy")
    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")
    staff_members = relationship("StaffMember", back_populates="role", cascade="all, delete-orphan")

    __table_args__ = (
        # Partial unique index for system roles (where pharmacy_id is null)
        Index("uq_system_role_name", "name", unique=True, postgresql_where=Column("pharmacy_id").is_(None)),
        # Partial unique index for custom roles per pharmacy (where pharmacy_id is not null)
        Index("uq_pharmacy_role_name", "pharmacy_id", "name", unique=True, postgresql_where=Column("pharmacy_id").is_not(None)),
    )


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(String, primary_key=True, default=new_uuid)
    code = Column(String, unique=True, nullable=False, index=True)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ORM Relationships
    roles = relationship("StaffRole", secondary="role_permissions", back_populates="permissions")


class RolePermission(Base):
    __tablename__ = "role_permissions"
    __table_args__ = (PrimaryKeyConstraint("role_id", "permission_id"),)

    role_id = Column(String, ForeignKey("staff_roles.id", ondelete="CASCADE"), nullable=False, index=True)
    permission_id = Column(String, ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False, index=True)


class StaffMember(Base):
    __tablename__ = "staff_members"

    id = Column(String, primary_key=True, default=new_uuid)
    pharmacy_id = Column(String, ForeignKey("pharmacies.id", ondelete="CASCADE"), nullable=False, index=True)
    branch_id = Column(String, ForeignKey("branches.id", ondelete="RESTRICT"), nullable=False, index=True)
    role_id = Column(String, ForeignKey("staff_roles.id", ondelete="RESTRICT"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    employee_code = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True, index=True)
    contact_email = Column(String, nullable=True, index=True)

    status = Column(String, default="active", nullable=False)  # active | disabled | terminated

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # ORM Relationships
    pharmacy = relationship("Pharmacy")
    branch = relationship("Branch")
    role = relationship("StaffRole", back_populates="staff_members")
    user = relationship("User")
    attendance_records = relationship("AttendanceRecord", back_populates="staff", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_staff_pharmacy_branch_status", "pharmacy_id", "branch_id", "status"),
        Index("uq_staff_pharmacy_email", "pharmacy_id", "contact_email", unique=True, postgresql_where=Column("contact_email").is_not(None)),
        Index("uq_staff_pharmacy_phone", "pharmacy_id", "contact_phone", unique=True, postgresql_where=Column("contact_phone").is_not(None)),
        Index("uq_staff_pharmacy_user", "pharmacy_id", "user_id", unique=True, postgresql_where=Column("user_id").is_not(None)),
    )


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id = Column(String, primary_key=True, default=new_uuid)
    pharmacy_id = Column(String, ForeignKey("pharmacies.id", ondelete="CASCADE"), nullable=False, index=True)
    branch_id = Column(String, ForeignKey("branches.id", ondelete="RESTRICT"), nullable=False, index=True)
    staff_id = Column(String, ForeignKey("staff_members.id", ondelete="RESTRICT"), nullable=False, index=True)

    check_in_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    check_out_at = Column(DateTime(timezone=True), nullable=True)
    working_minutes = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # ORM Relationships
    pharmacy = relationship("Pharmacy")
    branch = relationship("Branch")
    staff = relationship("StaffMember", back_populates="attendance_records")

    __table_args__ = (
        Index("uq_staff_active_checkin", "staff_id", unique=True, postgresql_where=Column("check_out_at").is_(None)),
        Index("ix_attendance_pharmacy_branch_dates", "pharmacy_id", "branch_id", "check_in_at"),
    )
