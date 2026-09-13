"""
app/staff/schemas.py

Pydantic v2 schemas for Staff Management, Roles, Permissions, and Attendance.
Reuses existing validation normalizers and enforces strict type guarantees.
"""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.pharmacy.schemas import normalize_optional_str, validate_and_normalize_phone
from app.staff.models import STAFF_STATUSES


class PermissionRead(BaseModel):
    id: str = Field(..., description="Unique UUID of the permission")
    code: str = Field(..., description="Unique permission code string (e.g. 'staff:write')")
    category: str = Field(..., description="Functional category (e.g. 'Billing', 'Inventory')")
    description: str | None = Field(None, description="Human-readable summary of the permission")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "abc-123-permission-uuid",
                "code": "staff:write",
                "category": "Staff Management",
                "description": "Add, update, disable, or terminate staff members and manage roles",
            }
        },
    )


class StaffRoleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the custom role")
    description: str | None = Field(None, max_length=500, description="Summary of role responsibilities")
    permissions: list[str] = Field(..., description="List of permission code strings assigned to this role")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Senior Cashier",
                "description": "Handles retail sales and returns with supervisory shift access",
                "permissions": ["billing:write", "attendance:read"],
            }
        }
    )

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, v: Any) -> Any:
        if v is None:
            raise ValueError("Name is required")
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("Name cannot be empty or only whitespace")
            return v
        raise ValueError("Name must be a string")

class StaffRoleUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100, description="Name of the custom role")
    description: str | None = Field(None, max_length=500, description="Summary of role responsibilities")
    permissions: list[str] | None = Field(None, description="List of permission code strings assigned to this role")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Senior Cashier v2",
                "description": "Updated retail sales permissions",
                "permissions": ["billing:write", "attendance:read"],
            }
        }
    )

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, v: Any) -> Any:
        if v is None:
            return None
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("Name cannot be empty or only whitespace")
            return v
        raise ValueError("Name must be a string")
class StaffRoleRead(BaseModel):
    id: str = Field(..., description="Unique UUID of the role")
    pharmacy_id: str | None = Field(None, description="UUID of the owning pharmacy (None if system role)")
    name: str = Field(..., description="Name of the role")
    description: str | None = Field(None, description="Summary of role responsibilities")
    is_system: bool = Field(..., description="Whether this is an immutable built-in system role")
    level: int = Field(..., description="Privilege hierarchy level")
    permissions: list[PermissionRead] = Field(..., description="Assigned granular permissions")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "role-uuid-1234",
                "pharmacy_id": "pharmacy-uuid-5678",
                "name": "Senior Cashier",
                "description": "Handles retail sales and returns with supervisory shift access",
                "is_system": False,
                "level": 10,
                "permissions": [
                    {
                        "id": "perm-uuid-1",
                        "code": "billing:write",
                        "category": "Billing",
                        "description": "Create, modify, and process point-of-sale billing invoices",
                    }
                ],
            }
        },
    )


class _StaffValidationMixin:
    """Shared normalizer mixin for Staff models."""

    @field_validator("contact_phone", mode="before")
    @classmethod
    def _val_phone(cls, v: Any) -> Any:
        return validate_and_normalize_phone(v)

    @field_validator("contact_email", mode="before")
    @classmethod
    def _val_email(cls, v: Any) -> Any:
        return normalize_optional_str(v)

    @field_validator("employee_code", "last_name", mode="before")
    @classmethod
    def _val_opt_strs(cls, v: Any) -> Any:
        return normalize_optional_str(v)


class StaffMemberCreate(_StaffValidationMixin, BaseModel):
    branch_id: str = Field(..., description="UUID of the branch where the employee works")
    role_id: str = Field(..., description="UUID of the role assigned to the employee")
    user_id: str | None = Field(None, description="Optional UUID of the linked User account for login authentication")
    employee_code: str | None = Field(None, max_length=50, description="Internal employee identification code/number")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name of the employee")
    last_name: str | None = Field(None, max_length=100, description="Last name of the employee")
    contact_phone: str | None = Field(None, max_length=20, description="Primary contact phone number (10-15 digits)")
    contact_email: EmailStr | None = Field(None, description="Primary contact email address")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "branch_id": "33cb179b-5023-4182-b6c8-ebb26e74a0f9",
                "role_id": "role-uuid-pharmacist",
                "user_id": "user-uuid-9999",
                "employee_code": "EMP-001",
                "first_name": "Rahul",
                "last_name": "Sharma",
                "contact_phone": "+919876543210",
                "contact_email": "rahul.sharma@medorax.com",
            }
        }
    )

    @field_validator("first_name", mode="before")
    @classmethod
    def validate_first_name(cls, v: Any) -> Any:
        if v is None:
            raise ValueError("first_name is required")
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("first_name cannot be empty or only whitespace")
            return v
        raise ValueError("first_name must be a string")


class StaffMemberUpdate(_StaffValidationMixin, BaseModel):
    branch_id: str | None = Field(None, description="New branch UUID")
    role_id: str | None = Field(None, description="New role UUID")
    user_id: str | None = Field(None, description="New linked User UUID")
    employee_code: str | None = Field(None, max_length=50, description="Updated employee code")
    first_name: str | None = Field(None, min_length=1, max_length=100, description="Updated first name")
    last_name: str | None = Field(None, max_length=100, description="Updated last name")
    contact_phone: str | None = Field(None, max_length=20, description="Updated phone number")
    contact_email: EmailStr | None = Field(None, description="Updated email address")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "role_id": "role-uuid-manager",
                "contact_phone": "+919876543211",
            }
        }
    )

    @field_validator("first_name", mode="before")
    @classmethod
    def validate_first_name(cls, v: Any) -> Any:
        if v is None or v == "" or (isinstance(v, str) and not v.strip()):
            return None
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("first_name cannot be empty or only whitespace")
            return v
        raise ValueError("first_name must be a string")


class StaffMemberStatusUpdate(BaseModel):
    status: str = Field(..., description="New employment status ('active', 'disabled', or 'terminated')")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "disabled"
            }
        }
    )

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v: Any) -> str:
        if isinstance(v, str):
            v = v.strip().lower()
        if v not in STAFF_STATUSES:
            raise ValueError(f"status must be one of {STAFF_STATUSES}")
        return v


class StaffMemberRead(BaseModel):
    id: str = Field(..., description="Unique UUID of the staff member record")
    pharmacy_id: str = Field(..., description="UUID of the parent pharmacy")
    branch_id: str = Field(..., description="UUID of the assigned branch")
    role_id: str = Field(..., description="UUID of the assigned role")
    user_id: str | None = Field(None, description="UUID of the linked login User account")
    employee_code: str | None = Field(None, description="Internal employee identification code")
    first_name: str = Field(..., description="First name")
    last_name: str | None = Field(None, description="Last name")
    contact_phone: str | None = Field(None, description="Contact phone number")
    contact_email: str | None = Field(None, description="Contact email address")
    status: str = Field(..., description="Employment status ('active', 'disabled', 'terminated')")
    role: StaffRoleRead | None = Field(None, description="Nested role and permissions object")
    created_at: datetime = Field(..., description="Record creation timestamp")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "staff-uuid-1111",
                "pharmacy_id": "11cb179b-5023-4182-b6c8-ebb26e74a0f7",
                "branch_id": "33cb179b-5023-4182-b6c8-ebb26e74a0f9",
                "role_id": "role-uuid-pharmacist",
                "user_id": "user-uuid-9999",
                "employee_code": "EMP-001",
                "first_name": "Rahul",
                "last_name": "Sharma",
                "contact_phone": "+919876543210",
                "contact_email": "rahul.sharma@medorax.com",
                "status": "active",
                "created_at": "2026-07-17T10:00:00Z",
            }
        },
    )


class AttendanceCheckIn(BaseModel):
    notes: str | None = Field(None, max_length=500, description="Optional check-in notes or shift identifier")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "notes": "Morning shift check-in"
            }
        }
    )


class AttendanceCheckOut(BaseModel):
    notes: str | None = Field(None, max_length=500, description="Optional check-out notes or shift handover summary")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "notes": "Completed dispensing duties cleanly"
            }
        }
    )


class AttendanceOverride(BaseModel):
    new_check_out_at: datetime = Field(..., description="Corrected or supervisor-assigned check-out timestamp (UTC)")
    override_reason: str = Field(..., min_length=1, max_length=500, description="Mandatory justification for manual shift modification")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "new_check_out_at": "2026-07-17T18:00:00Z",
                "override_reason": "Employee forgot to click check-out before leaving for emergency personal appointment",
            }
        }
    )


class AttendanceRead(BaseModel):
    id: str = Field(..., description="Unique UUID of the attendance record")
    pharmacy_id: str = Field(..., description="UUID of the parent pharmacy")
    branch_id: str = Field(..., description="UUID of the branch where attendance occurred")
    staff_id: str = Field(..., description="UUID of the staff member")
    check_in_at: datetime = Field(..., description="Timestamp of check-in (UTC)")
    check_out_at: datetime | None = Field(None, description="Timestamp of check-out (UTC)")
    working_minutes: int | None = Field(None, description="Total working duration in minutes computed upon check-out")
    notes: str | None = Field(None, description="Shift notes or override justification")
    created_at: datetime = Field(..., description="Record creation timestamp")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "attendance-uuid-7777",
                "pharmacy_id": "11cb179b-5023-4182-b6c8-ebb26e74a0f7",
                "branch_id": "33cb179b-5023-4182-b6c8-ebb26e74a0f9",
                "staff_id": "staff-uuid-1111",
                "check_in_at": "2026-07-17T09:00:00Z",
                "check_out_at": "2026-07-17T17:00:00Z",
                "working_minutes": 480,
                "notes": "Morning shift check-in",
                "created_at": "2026-07-17T09:00:00Z",
            }
        },
    )
