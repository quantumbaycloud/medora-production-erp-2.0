"""
app/staff/permissions.py

Centralized definitions for granular system permissions and immutable system roles.
Used across role seeding, vertical privilege checking, and endpoint RBAC enforcement.
"""

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class PermissionDefinition:
    code: str
    category: str
    description: str
    requires_sod: bool = False  # Flag for Segregation of Duties checks


class Permissions:
    # Staff & Role Operations
    STAFF_READ: Final = PermissionDefinition("staff:read", "Staff Management", "View staff profiles, roles, and branch assignments")
    STAFF_MANAGE: Final = PermissionDefinition("staff:manage", "Staff Management", "Add, update, disable, or terminate staff profiles")
    STAFF_ASSIGN_ROLE: Final = PermissionDefinition("staff:assign_role", "Staff Management", "Assign or modify security roles on staff within hierarchy limits")
    ROLE_MANAGE: Final = PermissionDefinition("role:manage", "IAM", "Create, update, and delete tenant custom roles")

    # Inventory & Procurement
    INVENTORY_MANAGE: Final = PermissionDefinition("inventory:manage", "Inventory", "Add stock batches, adjust pricing, and record expiries")
    INVENTORY_AUDIT: Final = PermissionDefinition("inventory:audit", "Inventory", "Execute physical stock reconciliations and write-offs")
    PURCHASE_CREATE: Final = PermissionDefinition("purchase:create", "Purchase", "Draft and submit supplier purchase orders")
    PURCHASE_APPROVE: Final = PermissionDefinition("purchase:approve", "Purchase", "Authorize inwards goods (GRN) into live inventory", requires_sod=True)

    # Sales & Billing
    BILLING_CREATE: Final = PermissionDefinition("billing:create", "Billing", "Generate point-of-sale customer invoices")
    BILLING_REFUND: Final = PermissionDefinition("billing:refund", "Billing", "Void invoices, process returns, and issue credit notes", requires_sod=True)

    # HR & Attendance
    ATTENDANCE_CHECKIN: Final = PermissionDefinition("attendance:checkin", "Attendance", "Record shift check-in and check-out timestamps")
    ATTENDANCE_OVERRIDE: Final = PermissionDefinition("attendance:override", "Attendance", "Manual check-out override for abandoned shifts", requires_sod=True)
    ATTENDANCE_READ: Final = PermissionDefinition("attendance:read", "Attendance", "View employee attendance records, shifts, and working hours")

    # Reports & Analytics
    REPORTS_READ: Final = PermissionDefinition("reports:read", "Reports", "Access financial, inventory, and operational summaries on screen")
    REPORTS_EXPORT: Final = PermissionDefinition("reports:export", "Reports", "Download bulk CSV/PDF financial and data reports")

    # Settings
    SETTINGS_UPDATE: Final = PermissionDefinition("settings:update", "Settings", "Configure pharmacy and branch operational toggles and preferences")

    # Drug Catalog
    MEDICINE_READ: Final = PermissionDefinition("medicine:read", "Medicine", "View drug catalog")
    MEDICINE_MANAGE: Final = PermissionDefinition("medicine:manage", "Medicine", "Add and update medicine entries")

    # Customers
    CUSTOMER_READ: Final = PermissionDefinition("customer:read", "Customer", "View customer profiles")
    CUSTOMER_MANAGE: Final = PermissionDefinition("customer:manage", "Customer", "Create and update customers")

    # Prescriptions
    PRESCRIPTION_READ: Final = PermissionDefinition("prescription:read", "Prescription", "View prescriptions")
    PRESCRIPTION_MANAGE: Final = PermissionDefinition("prescription:manage", "Prescription", "Upload and process prescriptions")

    # Audit & Compliance
    AUDIT_READ: Final = PermissionDefinition("audit:read", "Audit", "View audit trail")
    AUDIT_EXPORT: Final = PermissionDefinition("audit:export", "Audit", "Export audit data")

    # Documents
    DOCUMENT_READ: Final = PermissionDefinition("document:read", "Document", "View documents")
    DOCUMENT_MANAGE: Final = PermissionDefinition("document:manage", "Document", "Upload and modify documents")

    # Notifications
    NOTIFICATION_READ: Final = PermissionDefinition("notification:read", "Notification", "View notifications")
    NOTIFICATION_MANAGE: Final = PermissionDefinition("notification:manage", "Notification", "Mark and dismiss notifications")

    @classmethod
    def all_definitions(cls) -> list[PermissionDefinition]:
        return [
            v for k, v in cls.__dict__.items()
            if isinstance(v, PermissionDefinition)
        ]


# Hierarchy levels: higher tier cannot be assigned/modified by lower tier employees.
SYSTEM_ROLES_CONFIG = [
    {
        "name": "Owner",
        "description": "Primary pharmacy business owner with unrestricted access across all branches",
        "level": 100,
        "permissions": [p.code for p in Permissions.all_definitions()],
    },
    {
        "name": "Admin",
        "description": "System administrator with full operations and staff management access",
        "level": 90,
        "permissions": [p.code for p in Permissions.all_definitions()],
    },
    {
        "name": "Manager",
        "description": "Branch or operational manager with comprehensive day-to-day supervisory permissions",
        "level": 80,
        "permissions": [p.code for p in Permissions.all_definitions()],
    },
    {
        "name": "Pharmacist",
        "description": "Licensed pharmacist handling dispensing, inventory management, and billing",
        "level": 50,
        "permissions": [
            Permissions.INVENTORY_MANAGE.code,
            Permissions.BILLING_CREATE.code,
            Permissions.REPORTS_READ.code,
            Permissions.ATTENDANCE_READ.code,
            Permissions.MEDICINE_READ.code,
            Permissions.MEDICINE_MANAGE.code,
            Permissions.CUSTOMER_READ.code,
            Permissions.CUSTOMER_MANAGE.code,
            Permissions.PRESCRIPTION_READ.code,
            Permissions.PRESCRIPTION_MANAGE.code,
            Permissions.NOTIFICATION_READ.code,
        ],
    },
    {
        "name": "Inventory Manager",
        "description": "Specialist responsible for stock levels, audits, and distributor orders",
        "level": 50,
        "permissions": [
            Permissions.INVENTORY_MANAGE.code,
            Permissions.PURCHASE_CREATE.code,
            Permissions.REPORTS_READ.code,
            Permissions.ATTENDANCE_READ.code,
            Permissions.MEDICINE_READ.code,
            Permissions.MEDICINE_MANAGE.code,
            Permissions.NOTIFICATION_READ.code,
        ],
    },
    {
        "name": "Purchase Manager",
        "description": "Specialist managing supplier relationships, purchase orders, and inwards goods",
        "level": 50,
        "permissions": [
            Permissions.PURCHASE_CREATE.code,
            Permissions.PURCHASE_APPROVE.code,
            Permissions.INVENTORY_MANAGE.code,
            Permissions.REPORTS_READ.code,
            Permissions.ATTENDANCE_READ.code,
            Permissions.MEDICINE_READ.code,
            Permissions.NOTIFICATION_READ.code,
        ],
    },
    {
        "name": "Cashier",
        "description": "Point-of-sale cashier processing customer transactions and receipts",
        "level": 20,
        "permissions": [
            Permissions.BILLING_CREATE.code,
            Permissions.ATTENDANCE_READ.code,
            Permissions.MEDICINE_READ.code,
            Permissions.CUSTOMER_READ.code,
            Permissions.NOTIFICATION_READ.code,
        ],
    },
]
