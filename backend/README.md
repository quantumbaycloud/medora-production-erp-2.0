# Medorax Unified Pharmacy ERP Backend

---

# ⚠️ Development Status

> **IMPORTANT NOTICE FOR ALL DEVELOPERS:**
>
> The Medorax ERP backend is currently **under active development and integration**. 
>
> Core backend capabilities have been unified across authentication, multi-tenant pharmacy management, inventory, purchasing, billing, reporting, notifications, audit/documents, and prescription processing. However, full system integration, cross-module security auditing, and comprehensive end-to-end business validation are **NOT fully complete**.
>
> **THE BACKEND IS CURRENTLY NOT READY FOR FRONTEND INTEGRATION AS A COMPLETE ERP.**
>
> Frontend developers must **NOT** assume that all documented endpoints are stable, complete, or ready for production consumption. Only endpoints and workflows explicitly marked with **`✅ READY FOR FRONTEND`** in this document should be considered for active UI development.
>
> All other endpoints must be treated as **`🚧 IN DEVELOPMENT`**, **`🔍 UNDER VALIDATION`**, or **`⚠️ NOT READY`**. Do **NOT** describe this backend as "production-ready" or "feature-complete."

---

## ⚠️ Frontend Integration Status & Guidance

Frontend engineers should reference this table before building UI components or binding forms to backend APIs:

| Business Domain | API Implemented | Business Logic Verified | Frontend Integration Readiness | Notes / Restrictions |
|---|---|---|---|---|
| **Authentication & Auth** | Yes | Yes | ✅ READY FOR FRONTEND | Core login, registration, and refresh tokens are stable. Password reset / email verification remain under validation. |
| **User Profile (`/users/me`)** | Yes | Yes | ✅ READY FOR FRONTEND | Profile viewing and updates are functional. |
| **Pharmacy & Branches** | Yes | Yes | ✅ READY FOR FRONTEND | Multi-branch creation, pharmacy profile, and branch switching are functional. |
| **Staff & RBAC** | Yes | Partial | 🔍 UNDER VALIDATION | Staff profile endpoints exist; full vertical permission enforcement across every sub-module is undergoing validation. |
| **Medicines & Batches** | Yes | Yes | ✅ READY FOR FRONTEND | Product catalog, batch creation, barcode/SKU indexing, and batch listings are verified. |
| **Suppliers** | Yes | Yes | ✅ READY FOR FRONTEND | CRUD operations for vendor directory are functional. |
| **Purchasing & GRN** | Yes | Yes | 🚧 IN DEVELOPMENT | Draft creation and purchase approval (inwarding to `MedicineBatch`) work; edit/cancel flows are under validation. |
| **Customers** | Yes | Yes | ✅ READY FOR FRONTEND | Customer directory and outstanding balance tracking are functional. |
| **Billing & Point of Sale** | Yes | Yes | 🚧 IN DEVELOPMENT | Standard cash/card billing, hold bills, and returns are functional; complex split-payment edge cases are under validation. |
| **Returns & Exchanges** | Yes | Yes | 🚧 IN DEVELOPMENT | Return bills and exchange calculations function; ledger synchronization is verified. |
| **Inventory & Ledger** | Yes | Yes | 🚧 IN DEVELOPMENT | Stock adjustments, ledger log retrieval, CSV import, and CSV/Excel/PDF export are functional. |
| **Settings** | Yes | Yes | ✅ READY FOR FRONTEND | Pharmacy settings GET and PATCH/PUT are verified with tenant isolation. |
| **Reports & Dashboard** | Yes | Partial | 🔍 UNDER VALIDATION | KPI calculation and Excel exports exist; financial precision under high-volume data is undergoing validation. |
| **Notifications & Alerts** | Yes | Partial | 🔍 UNDER VALIDATION | In-app notification listing and read toggles work; Celery Beat background scheduler requires live Redis in target environment. |
| **Audit & Documents** | Yes | Partial | 🔍 UNDER VALIDATION | S3 document upload/download is verified; queryable audit log filtering is implemented but undergoing UI contract validation. |
| **Prescriptions & AI/OCR** | Yes | Partial | 🟡 EXTERNAL DEPENDENCY | Manual review endpoints work; automated PaddleOCR and LLM extraction require external API credentials and system dependencies. |

---

## Table of Contents
1. [Core Purpose & Architecture Overview](#1-core-purpose--architecture-overview)
2. [Source Code & Directory Structure](#2-source-code--directory-structure)
3. [Technology Stack & System Requirements](#3-technology-stack--system-requirements)
4. [Database Architecture & Canonical Data Models](#4-database-architecture--canonical-data-models)
5. [Transaction Management & Persistence Architecture](#5-transaction-management--persistence-architecture)
6. [Authentication, Sessions & Security](#6-authentication-sessions--security)
7. [Staff Management, RBAC & Multi-Tenancy](#7-staff-management-rbac--multi-tenancy)
8. [Core Business Workflows](#8-core-business-workflows)
9. [Comprehensive API Reference](#9-comprehensive-api-reference)
10. [Detailed Request & Response Contracts](#10-detailed-request--response-contracts)
11. [Background Tasks & Scheduling](#11-background-tasks--scheduling)
12. [Prescription Intelligence & Clinical Safety](#12-prescription-intelligence--clinical-safety)
13. [Intentionally Excluded Components](#13-intentionally-excluded-components)
14. [Local Development Setup](#14-local-development-setup)
15. [Environment Configuration Reference](#15-environment-configuration-reference)
16. [Remaining Work & Technical Roadmap](#16-remaining-work--technical-roadmap)

---

## 1. Core Purpose & Architecture Overview

The Medorax ERP backend is a multi-tenant enterprise pharmacy management system built to handle day-to-day retail and multi-branch pharmacy operations, including point-of-sale billing, inventory control, purchase order inwards (GRN), compliance tracking, financial reporting, and clinical safety checks.

### High-Level Request Flow
```text
HTTP Request (Client)
    │
    ▼
[ RequestIDMiddleware ] (Generates X-Request-ID)
    │
    ▼
[ slowapi Limiter ] (Rate Limiting)
    │
    ▼
[ FastAPI Router ] (Prefix & Tag Scoping)
    │
    ▼
[ Security & Dependencies ]
    ├── get_current_user (JWT validation, session status, password revocation)
    ├── get_current_pharmacy_id (Multi-tenant context resolution)
    └── Permissions Check (Vertical RBAC & Segregation of Duties)
    │
    ▼
[ Pydantic Schema Validation ] (Request Body / Query Parsing)
    │
    ▼
[ Service Layer ] (Business Logic Execution & db.flush())
    │
    ▼
[ Repository / SQLAlchemy ORM ] (PostgreSQL Query Execution)
    │
    ▼
[ get_db Dependency Teardown ] (Atomic db.commit() on success, db.rollback() on exception)
    │
    ▼
HTTP Response (Pydantic ResponseModel Serialized)
```

---

## 2. Source Code & Directory Structure

The core application code is located in `medorax-erp-backend/app/`:

```text
medorax-erp-backend/
├── app/
│   ├── auth/              # Registration, login, JWT tokens, session & device tracking
│   │   ├── models.py      # User credentials, sessions, login history, tokens
│   │   ├── router.py      # /auth and /internal endpoints
│   │   ├── schemas.py     # Auth request/response models
│   │   └── service.py     # Password hashing, token generation, session lifecycle
│   │
│   ├── user/              # User account profile management
│   │   ├── models.py      # Base User identity model
│   │   ├── router.py      # /users/me endpoints
│   │   └── schemas.py     # UserRead, UserUpdate schemas
│   │
│   ├── pharmacy/          # Pharmacy business entity & ownership profiles
│   │   ├── models.py      # Pharmacy, PharmacyOwner models
│   │   ├── router.py      # /pharmacies endpoints
│   │   └── schemas.py     # PharmacyCreate, PharmacyResponse
│   │
│   ├── branch/            # Multi-branch management per pharmacy
│   │   ├── models.py      # Branch entity model
│   │   ├── router.py      # /branches endpoints
│   │   └── schemas.py     # BranchCreate, BranchResponse
│   │
│   ├── staff/             # Employee profiles, role hierarchy, shift attendance
│   │   ├── models.py      # Staff, Role, Attendance, StaffBranchAssignment
│   │   ├── permissions.py # Centralized permission codes & system roles config
│   │   ├── router.py      # /staff, /roles, /attendance endpoints
│   │   ├── schemas.py     # StaffCreate, RoleResponse, AttendanceCheckIn
│   │   └── service.py     # Multi-tenant context extraction & permission checks
│   │
│   ├── medicine/          # Drug catalog and pharmaceutical specifications
│   │   ├── models.py      # Medicine, MedicineBatch canonical models
│   │   ├── repository.py  # Medicine search and query filters
│   │   ├── router.py      # /medicines endpoints
│   │   └── schemas.py     # MedicineCreate, MedicineBatchResponse
│   │
│   ├── inventory/         # Stock adjustments, ledger history, imports & exports
│   │   ├── models.py      # InventoryLedger model
│   │   ├── repository.py  # Ledger query execution
│   │   ├── router.py      # /inventory/ledger, /adjust, /export, /import
│   │   ├── schemas.py     # StockAdjustmentCreate, InventoryLedgerResponse
│   │   ├── service.py     # Stock adjustment logic
│   │   └── services/      # export_service.py (CSV/Excel/PDF), import_service.py
│   │
│   ├── supplier/          # Vendor and distributor directory
│   │   ├── models.py      # Supplier entity model
│   │   ├── repository.py  # Supplier database queries
│   │   ├── router.py      # /suppliers endpoints
│   │   └── schemas.py     # SupplierCreate, SupplierResponse
│   │
│   ├── purchase/          # Procurement, Purchase Orders, and GRN Inwards
│   │   ├── models.py      # PurchaseInvoice, PurchaseItem models
│   │   ├── repository.py  # Purchase queries and filters
│   │   ├── router.py      # /purchases endpoints
│   │   ├── schemas.py     # PurchaseInvoiceCreate, PurchaseInvoiceResponse
│   │   └── service.py     # Order drafting and approval with batch creation
│   │
│   ├── customer/          # Retail and credit customer management
│   │   ├── models.py      # Customer entity model
│   │   ├── repository.py  # Customer queries and balance calculations
│   │   ├── router.py      # /customers endpoints
│   │   └── schemas.py     # CustomerCreate, CustomerResponse
│   │
│   ├── billing/           # Point-of-Sale (POS), invoicing, returns, exchanges, hold cart
│   │   ├── models.py      # Invoice, InvoiceItem, HoldBill, ReturnBill, ExchangeBill
│   │   ├── repository.py  # Invoice retrieval
│   │   ├── router.py      # /billing/invoice, /quick, /hold, /returns, /exchanges
│   │   ├── schemas.py     # GenerateInvoiceRequest, InvoiceResponse, ReturnBillCreate
│   │   └── services/      # billing_service.py, return_service.py, exchange_service.py
│   │
│   ├── audit/             # Compliance audit trail and document metadata
│   │   ├── models.py      # AuditLog, DocumentMetadata models
│   │   ├── router.py      # /audit-logs, /documents endpoints
│   │   ├── schemas.py     # AuditLogResponse, DocumentResponse
│   │   └── service.py     # Audit persistence and S3 document uploads
│   │
│   ├── reports/           # Financial analytics, tax summaries, periodic alert tasks
│   │   ├── router.py      # /reports/dashboard, /sales, /expiry, /gst
│   │   ├── schemas.py     # DashboardKPIResponse, SalesReportItem, GSTReportItem
│   │   ├── service.py     # KPI aggregation and pandas Excel generation
│   │   └── tasks.py       # check_low_stock_and_expiry periodic background task
│   │
│   ├── notifications/     # In-app system alerts and notifications
│   │   ├── models.py      # Notification model
│   │   ├── router.py      # /notifications endpoints
│   │   ├── schemas.py     # NotificationResponse
│   │   └── service.py     # Alert creation, read toggles, and deduplication
│   │
│   ├── settings/          # Pharmacy operational parameters and compliance config
│   │   ├── models.py      # PharmacySetting model
│   │   ├── router.py      # /settings endpoints
│   │   ├── schemas.py     # SettingResponse, SettingUpdate
│   │   └── service.py     # Configuration retrieval and persistent update
│   │
│   ├── prescription/      # Prescription scanning, OCR, AI analysis, clinical safety
│   │   ├── models.py      # Prescription entity model
│   │   ├── router.py      # /prescriptions/upload, /analysis, /drug-interactions
│   │   ├── schemas.py     # PrescriptionResponse, HumanReviewRequest
│   │   ├── tasks.py       # process_prescription_task (Celery background worker)
│   │   └── services/      # ocr_service.py, ai_service.py, clinical_safety_service.py
│   │
│   ├── core/              # Core infrastructure configuration
│   │   ├── config.py      # Pydantic BaseSettings loading from .env
│   │   ├── celery_app.py  # Celery & Celery Beat broker/schedule configuration
│   │   ├── storage.py     # Boto3 MinIO/S3 object storage client
│   │   ├── exceptions.py  # Standard domain exceptions (NotFoundException, etc.)
│   │   └── logging_config.py # Structured JSON logging
│   │
│   ├── db/                # Database engine and session lifecycle
│   │   └── base.py        # SQLAlchemy engine, SessionLocal, get_db generator
│   │
│   └── shared/            # Common dependencies, middleware, and rate limiting
│       ├── deps.py        # get_current_user JWT dependency
│       ├── middleware.py  # RequestID tracking middleware
│       └── rate_limit.py  # slowapi limiter instance
│
├── migrations/            # Alembic database migration scripts
│   ├── env.py
│   └── versions/
├── alembic.ini
├── requirements.txt
└── .env.example
```

---

## 3. Technology Stack & System Requirements

- **Backend Framework:** FastAPI (Python 3.11+)
- **ORM / Database Layer:** SQLAlchemy 2.0 (Declarative Mapping)
- **Database Engine:** PostgreSQL 15+ (with `psycopg` binary driver)
- **Database Migrations:** Alembic
- **Task Queue & Scheduling:** Celery 5.x + Redis 7.x (with Celery Beat)
- **Object Storage:** AWS S3 / MinIO (via `boto3`)
- **Data Export & Reporting:** Pandas, XlsxWriter, OpenPyXL, ReportLab (PDF)
- **Authentication & Security:** Argon2id (`argon2-cffi`), PyJWT, slowapi (Rate Limiting)
- **Document OCR / AI (Optional / External):** OpenCV Headless, PaddleOCR, OpenAI Client

---

## 4. Database Architecture & Canonical Data Models

All monetary fields are strictly defined using `Numeric(10, 2)` to eliminate floating-point rounding errors. Entity identifiers use standard 36-character UUID strings (`new_uuid()`).

### The Canonical Medicine & Batch Architecture
To prevent inventory duplication and support accurate FIFO batch pricing, inventory is strictly split into two layers:

1. **`Medicine` (Product Catalog Layer):**
   - Stores static product attributes: `name`, `generic_name`, `brand_name`, `manufacturer`, `category`, `unit`, `hsn_code`, `gst_percentage`, `min_stock_level`, `rack`, `barcode`, `sku`.
   - Scoped to `pharmacy_id`.
2. **`MedicineBatch` (Physical Inventory Layer):**
   - Stores variable batch parameters: `batch_number`, `expiry_date`, `purchase_price`, `selling_price`, `mrp`, `quantity_available`, `status` (`ACTIVE`, `EXPIRED`, `QUARANTINED`).
   - Foreign-keyed to `medicines.id`.

### Core Database Entities

```mermaid
erDiagram
    Pharmacy ||--o{ Branch : owns
    Pharmacy ||--o{ Staff : employs
    Pharmacy ||--o{ Medicine : catalogs
    Medicine ||--o{ MedicineBatch : contains
    Pharmacy ||--o{ Supplier : contracts
    Supplier ||--o{ PurchaseInvoice : supplies
    PurchaseInvoice ||--o{ PurchaseItem : items
    Pharmacy ||--o{ Customer : registers
    Pharmacy ||--o{ Invoice : issues
    Invoice ||--o{ InvoiceItem : items
    Pharmacy ||--o{ InventoryLedger : tracks
    Pharmacy ||--o{ AuditLog : records
    Pharmacy ||--o{ DocumentMetadata : stores
    Pharmacy ||--o{ Notification : alerts
    Pharmacy ||--o{ PharmacySetting : configures
    Pharmacy ||--o{ Prescription : processes
```

- **`InventoryLedger`:** Immutable audit log of all physical stock movements (`transaction_type`: `PURCHASE`, `SALE`, `RETURN`, `ADJUSTMENT`, `LOSS`, `EXPIRED`).
- **`AuditLog`:** Compliance trail capturing user actions, IP addresses, entity mutations, and JSON metadata.
- **`DocumentMetadata`:** Uploaded certificates, licenses, and bills with expiration dates and S3 object keys.
- **`PharmacySetting`:** Tenant-isolated operational toggles (GST percentages, invoice templates, session timeouts, maintenance mode).

---

## 5. Transaction Management & Persistence Architecture

The backend implements a strict, leak-free transaction lifecycle managed at the request dependency boundary in `app/db/base.py`:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()  # Automatically commits on successful HTTP 2xx
    except Exception:
        db.rollback()  # Automatically rolls back on unhandled error
        raise
    finally:
        db.close()
```

### Critical Rules for Backend Developers
1. **Never call `db.commit()` inside standard request services.** Service methods must only call `db.flush()` to populate auto-generated IDs and trigger constraints. The `get_db` generator commits the transaction once the router finishes successfully.
2. **Background Tasks Own Their Sessions:** Asynchronous Celery tasks run outside the HTTP request lifecycle and must instantiate their own context-managed `SessionLocal()` block with explicit `try...commit...except...rollback...finally...close` blocks.
3. **Pessimistic Concurrency Locking:** To prevent inventory race conditions during simultaneous checkout and inwards goods, all batch stock updates must lock the target row using `.with_for_update()`.

---

## 6. Authentication, Sessions & Security

### Authentication Headers
All protected API endpoints require an `Authorization` header containing an active JWT Bearer token:
```http
Authorization: Bearer <access_token>
```

### Multi-Tenant Context Header / Query
For multi-branch or multi-pharmacy accounts, pass the target tenant context:
```http
GET /inventory/ledger?pharmacy_id=<pharmacy_uuid>
```
*If omitted, the backend falls back to the user's primary assigned pharmacy.*

### Token Lifecycles
- **Access Tokens:** Short-lived (Default: 15 minutes).
- **Refresh Tokens:** Long-lived (Default: 30 days), stored in the database with device tracking.
- **Password Revocation:** Modifying a user's password updates `users.password_updated_at`. Any active access token issued prior to that timestamp is immediately rejected by the auth dependency.

---

## 7. Staff Management, RBAC & Multi-Tenancy

Role-Based Access Control is enforced through granular permission definitions located in `app/staff/permissions.py`.

### System Role Hierarchy
1. **Owner (`level: 100`):** Unrestricted access across all pharmacy branches.
2. **Admin (`level: 90`):** Full operational, financial, and staff management permissions.
3. **Manager (`level: 80`):** Supervisory permissions over inventory, billing, and branch staff.
4. **Pharmacist (`level: 50`):** Dispensing, inventory adjustments, point-of-sale billing, and prescription review.
5. **Inventory Manager (`level: 50`):** Stock reconciliations, procurement drafting, and batch tracking.
6. **Purchase Manager (`level: 50`):** Purchase drafting and goods inward authorization (`purchase:approve`).
7. **Cashier (`level: 20`):** Retail point-of-sale checkout and receipt printing.

### Segregation of Duties (SoD)
Certain sensitive operational permissions are marked `requires_sod=True` (e.g., `purchase:approve`, `billing:refund`, `attendance:override`). A single user cannot draft and unilaterally approve high-value transactions without explicit role authorization.

---

## 8. Core Business Workflows

### 1. Purchase Inwards (GRN Flow)
```text
POST /purchases (Draft Purchase Created)
    │
    ▼
POST /purchases/{id}/approve (Authorize GRN)
    ├── Checks PURCHASE_APPROVE permission
    ├── Locks existing batch rows via .with_for_update()
    ├── Updates existing batch quantity OR creates new MedicineBatch (status='ACTIVE')
    ├── Updates purchase status to 'APPROVED'
    └── Records AuditLog entry ('PURCHASE_APPROVED')
```

### 2. Retail Billing & Stock Deduction Flow
```text
POST /billing/invoice (Checkout)
    ├── Checks BILLING_CREATE permission
    ├── Verifies item availability and locks batch rows (.with_for_update())
    ├── Deducts quantity from MedicineBatch.quantity_available
    ├── Writes InventoryLedger row (transaction_type='SALE', quantity=-N)
    ├── Records payment split (Cash / Card / UPI / Wallet / Credit)
    ├── Inserts Invoice and InvoiceItem records
    └── Records AuditLog entry ('INVOICE_CREATED')
```

### 3. Return & Stock Restoration Flow
```text
POST /billing/returns (Process Customer Return)
    ├── Verifies original invoice number and returned quantity
    ├── Locks batch row (.with_for_update())
    ├── Restores quantity to MedicineBatch.quantity_available
    ├── Writes InventoryLedger row (transaction_type='RETURN', quantity=+N)
    ├── Inserts ReturnBill record with refund amount
    └── Records AuditLog entry ('RETURN_PROCESSED')
```

---

## 9. Comprehensive API Reference

### Authentication & User Management
| Method | Endpoint | Description | Auth Required | Status |
|---|---|---|---|---|
| `POST` | `/auth/register` | Register a new user account | No | ✅ READY FOR FRONTEND |
| `POST` | `/auth/login` | Authenticate credentials & retrieve access/refresh tokens | No | ✅ READY FOR FRONTEND |
| `POST` | `/auth/refresh` | Exchange refresh token for a new access token | No | ✅ READY FOR FRONTEND |
| `POST` | `/auth/logout` | Revoke active session | Yes | ✅ READY FOR FRONTEND |
| `POST` | `/auth/forgot-password` | Request password reset email | No | 🔍 UNDER VALIDATION |
| `POST` | `/auth/reset-password` | Reset password using verified token | No | 🔍 UNDER VALIDATION |
| `GET` | `/users/me` | Retrieve current user profile | Yes | ✅ READY FOR FRONTEND |
| `PATCH` | `/users/me` | Update current user profile | Yes | ✅ READY FOR FRONTEND |

### Pharmacy & Branch Management
| Method | Endpoint | Description | Auth Required | Status |
|---|---|---|---|---|
| `POST` | `/pharmacies` | Create new pharmacy business profile | Yes | ✅ READY FOR FRONTEND |
| `GET` | `/pharmacies` | List pharmacies owned by or assigned to user | Yes | ✅ READY FOR FRONTEND |
| `GET` | `/pharmacies/{id}` | Retrieve specific pharmacy profile | Yes | ✅ READY FOR FRONTEND |
| `PATCH` | `/pharmacies/{id}` | Update pharmacy details | Yes | ✅ READY FOR FRONTEND |
| `POST` | `/branches` | Create a new branch under a pharmacy | Yes | ✅ READY FOR FRONTEND |
| `GET` | `/branches` | List all branches for active pharmacy | Yes | ✅ READY FOR FRONTEND |
| `GET` | `/branches/{id}` | Retrieve branch profile | Yes | ✅ READY FOR FRONTEND |
| `PATCH` | `/branches/{id}` | Update branch details | Yes | ✅ READY FOR FRONTEND |

### Staff, Roles & Attendance
| Method | Endpoint | Description | Auth Required | Status |
|---|---|---|---|---|
| `GET` | `/staff` | List employee directory | Yes | 🔍 UNDER VALIDATION |
| `POST` | `/staff` | Onboard new staff member | Yes | 🔍 UNDER VALIDATION |
| `GET` | `/roles` | List available system and custom roles | Yes | 🔍 UNDER VALIDATION |
| `POST` | `/attendance/checkin` | Record shift clock-in | Yes | 🔍 UNDER VALIDATION |
| `POST` | `/attendance/checkout` | Record shift clock-out | Yes | 🔍 UNDER VALIDATION |

### Medicine Catalog & Batches
| Method | Endpoint | Description | Auth Required | Status |
|---|---|---|---|---|
| `POST` | `/medicines` | Create catalog medicine entry | Yes | ✅ READY FOR FRONTEND |
| `GET` | `/medicines` | Search and list medicines | Yes | ✅ READY FOR FRONTEND |
| `GET` | `/medicines/{id}` | Retrieve medicine details | Yes | ✅ READY FOR FRONTEND |
| `PATCH` | `/medicines/{id}` | Update medicine catalog details | Yes | ✅ READY FOR FRONTEND |
| `POST` | `/medicines/{id}/batches` | Add a new stock batch to a medicine | Yes | ✅ READY FOR FRONTEND |
| `GET` | `/medicines/{id}/batches` | List active inventory batches for a medicine | Yes | ✅ READY FOR FRONTEND |

### Inventory, Stock Adjustments, Import & Export
| Method | Endpoint | Description | Auth Required | Status |
|---|---|---|---|---|
| `GET` | `/inventory/ledger` | Query stock movement audit trail | Yes | 🚧 IN DEVELOPMENT |
| `POST` | `/inventory/adjust` | Record manual physical stock reconciliation | Yes | 🚧 IN DEVELOPMENT |
| `POST` | `/inventory/import/medicines` | Bulk import medicines and batches via CSV | Yes | 🚧 IN DEVELOPMENT |
| `GET` | `/inventory/export/{entity}` | Export entity data (`medicines`, `ledger`, `suppliers`) as CSV/Excel/PDF | Yes | 🚧 IN DEVELOPMENT |

### Suppliers & Procurement (Purchases)
| Method | Endpoint | Description | Auth Required | Status |
|---|---|---|---|---|
| `POST` | `/suppliers` | Create supplier profile | Yes | ✅ READY FOR FRONTEND |
| `GET` | `/suppliers` | List registered suppliers | Yes | ✅ READY FOR FRONTEND |
| `GET` | `/suppliers/{id}` | Retrieve supplier profile | Yes | ✅ READY FOR FRONTEND |
| `PATCH` | `/suppliers/{id}` | Update supplier profile | Yes | ✅ READY FOR FRONTEND |
| `POST` | `/purchases` | Create draft purchase invoice | Yes | 🚧 IN DEVELOPMENT |
| `GET` | `/purchases` | List purchase orders with status filter | Yes | 🚧 IN DEVELOPMENT |
| `GET` | `/purchases/{id}` | Retrieve purchase invoice with line items | Yes | 🚧 IN DEVELOPMENT |
| `POST` | `/purchases/{id}/approve` | Inward goods (GRN) into active inventory batches | Yes | 🚧 IN DEVELOPMENT |

### Customers
| Method | Endpoint | Description | Auth Required | Status |
|---|---|---|---|---|
| `POST` | `/customers` | Register customer profile | Yes | ✅ READY FOR FRONTEND |
| `GET` | `/customers` | List and search customer directory | Yes | ✅ READY FOR FRONTEND |
| `GET` | `/customers/{id}` | Retrieve customer profile | Yes | ✅ READY FOR FRONTEND |
| `PATCH` | `/customers/{id}` | Update customer profile | Yes | ✅ READY FOR FRONTEND |
| `GET` | `/customers/{id}/outstanding` | Retrieve credit balance summary | Yes | ✅ READY FOR FRONTEND |

### Billing, Point of Sale (POS), Returns & Exchanges
| Method | Endpoint | Description | Auth Required | Status |
|---|---|---|---|---|
| `POST` | `/billing/invoice` | Generate final sale invoice & deduct stock | Yes | 🚧 IN DEVELOPMENT |
| `POST` | `/billing/quick` | Single-item rapid checkout | Yes | 🚧 IN DEVELOPMENT |
| `POST` | `/billing/hold` | Park an active transaction cart | Yes | 🚧 IN DEVELOPMENT |
| `GET` | `/billing/hold/{hold_number}` | Retrieve parked cart for checkout resumption | Yes | 🚧 IN DEVELOPMENT |
| `POST` | `/billing/returns` | Process medicine return & restore batch stock | Yes | 🚧 IN DEVELOPMENT |
| `POST` | `/billing/exchanges` | Exchange item and calculate price differential | Yes | 🚧 IN DEVELOPMENT |
| `GET` | `/invoices/{invoice_number}` | Retrieve invoice receipt | Yes | 🚧 IN DEVELOPMENT |

### Reports & Financial Summaries
| Method | Endpoint | Description | Auth Required | Status |
|---|---|---|---|---|
| `GET` | `/reports/dashboard` | 10 real-time KPIs (Today sales, stock alerts, profits) | Yes | 🔍 UNDER VALIDATION |
| `GET` | `/reports/sales` | Sales breakdown (Daily/Weekly/Monthly/Yearly/Branch) | Yes | 🔍 UNDER VALIDATION |
| `GET` | `/reports/expiry` | Inventory expiry report with days-ahead filter | Yes | 🔍 UNDER VALIDATION |
| `GET` | `/reports/gst` | GST / HSN tax breakdown report | Yes | 🔍 UNDER VALIDATION |

### Notifications & System Alerts
| Method | Endpoint | Description | Auth Required | Status |
|---|---|---|---|---|
| `GET` | `/notifications` | List in-app notifications & low-stock alerts | Yes | 🔍 UNDER VALIDATION |
| `PATCH` | `/notifications/{id}/read` | Mark notification as read | Yes | 🔍 UNDER VALIDATION |
| `POST` | `/notifications/mark-all-read` | Mark all notifications as read | Yes | 🔍 UNDER VALIDATION |

### Pharmacy Settings
| Method | Endpoint | Description | Auth Required | Status |
|---|---|---|---|---|
| `GET` | `/settings` | Retrieve active pharmacy configuration | Yes | ✅ READY FOR FRONTEND |
| `PATCH` | `/settings` | Update invoice templates, GST rates, and session rules | Yes | ✅ READY FOR FRONTEND |

### Compliance Audit Trail & Documents
| Method | Endpoint | Description | Auth Required | Status |
|---|---|---|---|---|
| `GET` | `/audit-logs` | Filter and view database audit trail | Yes | 🔍 UNDER VALIDATION |
| `GET` | `/documents` | List uploaded compliance documents | Yes | 🔍 UNDER VALIDATION |
| `POST` | `/documents/upload` | Upload document to S3/MinIO with metadata | Yes | 🔍 UNDER VALIDATION |
| `GET` | `/documents/{id}/download` | Generate time-limited presigned S3 download URL | Yes | 🔍 UNDER VALIDATION |

### Prescriptions & Clinical Safety
| Method | Endpoint | Description | Auth Required | Status |
|---|---|---|---|---|
| `POST` | `/prescriptions/upload` | Upload prescription image to storage | Yes | 🟡 EXTERNAL DEPENDENCY |
| `GET` | `/prescriptions/{id}/analysis` | Retrieve structured OCR/AI extraction result | Yes | 🟡 EXTERNAL DEPENDENCY |
| `POST` | `/prescriptions/{id}/human-review` | Submit pharmacist review / approval | Yes | ✅ READY FOR FRONTEND |
| `POST` | `/prescriptions/drug-interactions` | Check drug-to-drug interactions across list | Yes | ✅ READY FOR FRONTEND |
| `POST` | `/prescriptions/allergy-warning` | Verify patient allergies against drug list | Yes | ✅ READY FOR FRONTEND |
| `POST` | `/prescriptions/generic-suggestions` | Retrieve generic equivalents for branded drugs | Yes | ✅ READY FOR FRONTEND |

---

## 10. Detailed Request & Response Contracts

### 1. Generate Invoice (Point of Sale)
- **Endpoint:** `POST /billing/invoice`
- **Authentication:** Bearer JWT Token
- **Required Permission:** `billing:create`
- **Status:** `🚧 IN DEVELOPMENT`

#### Request Body
```json
{
  "customer_id": "optional-customer-uuid",
  "customer_name": "Walk-in Customer",
  "branch_id": "optional-branch-uuid",
  "payment_method": "Split Payment",
  "is_credit": false,
  "cash_amount": 100.00,
  "card_amount": 140.00,
  "upi_amount": 0.00,
  "wallet_amount": 0.00,
  "items": [
    {
      "medicine_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "batch_number": "BAT-AUG-01",
      "quantity": 2,
      "discount_type": "percentage",
      "discount_value": 5.00
    }
  ]
}
```

#### Response (`HTTP 201 Created`)
```json
{
  "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "pharmacy_id": "13717df1-8d15-46b8-a23b-4233b5933156",
  "branch_id": null,
  "customer_id": null,
  "invoice_number": "INV-20260823-9912",
  "invoice_date": "2026-08-23T17:07:03.844Z",
  "customer_name": "Walk-in Customer",
  "total_amount": 240.00,
  "discount_amount": 12.00,
  "tax_amount": 24.00,
  "payment_method": "Split Payment",
  "payment_status": "Paid",
  "items": [
    {
      "id": "e2f11a43-85b4-4b53-a532-678912345678",
      "medicine_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "medicine_name": "Augmentin 625mg",
      "batch_number": "BAT-AUG-01",
      "quantity": 2,
      "rate": 120.00,
      "discount": 12.00,
      "gst_percentage": 12.00,
      "gst_amount": 24.00,
      "total_amount": 240.00
    }
  ]
}
```

---

### 2. Create & Inward Purchase Order (GRN)
- **Endpoint:** `POST /purchases/{id}/approve`
- **Authentication:** Bearer JWT Token
- **Required Permission:** `purchase:approve` (Requires Segregation of Duties)
- **Status:** `🚧 IN DEVELOPMENT`

#### Response (`HTTP 200 OK`)
```json
{
  "id": "4a73b22e-1123-4567-89ab-cdef01234567",
  "pharmacy_id": "13717df1-8d15-46b8-a23b-4233b5933156",
  "supplier_id": "8b821173-b911-4aa0-a3f1-94f5ccfa6b30",
  "invoice_number": "PINV-SUP-8891",
  "invoice_date": "2026-08-23",
  "total_amount": 1000.00,
  "paid_amount": 1000.00,
  "is_paid": true,
  "status": "APPROVED",
  "items": [
    {
      "id": "992a11b3-4421-4112-9901-aabbccddeeff",
      "medicine_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "batch_number": "BAT-AUG-02",
      "expiry_date": "2028-12-31",
      "quantity": 100,
      "free_quantity": 10,
      "purchase_price": 8.00,
      "selling_price": 12.00,
      "mrp": 15.00,
      "total_amount": 840.00
    }
  ]
}
```

---

## 11. Background Tasks & Scheduling

The backend utilizes **Celery** backed by **Redis** for asynchronous processing and scheduled cron maintenance:

1. **Daily Stock & Expiry Check (`check_low_stock_and_expiry`):**
   - **Trigger:** Celery Beat schedule (Every 24 hours).
   - **Logic:** Scans all active pharmacies for batches with `expiry_date <= Today + 30 Days` and `quantity_available <= Medicine.min_stock_level`.
   - **Deduplication:** Verifies that an unread notification does not already exist for that specific batch before creating a new `Notification` row.
2. **Prescription Processing Worker (`process_prescription_task`):**
   - **Trigger:** Celery async task queued on prescription upload.
   - **Logic:** Downloads image from S3, executes OpenCV preprocessing + PaddleOCR text extraction, runs LLM parsing with regex fallback, matches against tenant inventory, and calculates clinical safety flags.

---

## 12. Prescription Intelligence & Clinical Safety

### Current Functional State
- **Clinical Safety Rules (`ClinicalSafetyService`):** ✅ **Fully Verified**. Standalone rule validation for drug-to-drug interactions (e.g. Warfarin + NSAIDs), allergy cross-sensitivity (e.g. Penicillin / Beta-lactams), and brand-to-generic substitutions works without external services.
- **Human Review Endpoint:** ✅ **Fully Verified**. Pharmacists can review extracted JSON, correct items, and approve/reject prescriptions.
- **PaddleOCR & LLM Pipeline:** 🟡 **External Dependency / In Progress**. The background processing worker handles fallback regex parsing cleanly, but local PaddleOCR execution and live LLM extraction require external API keys (`LLM_API_KEY`) and OCR inference binaries.

---

## 13. Intentionally Excluded Components

To maintain architectural integrity and prevent duplicate sources of truth, the following source components were deliberately excluded from the unified backend:

1. **Standalone Django Inventory Prototype:**
   - The repository previously contained an experimental Django-based inventory implementation.
   - **Reason for Exclusion:** The unified backend standardizes on FastAPI + SQLAlchemy + PostgreSQL. Integrating Django would introduce conflicting ORMs, dual database schemas, duplicate inventory tables, and broken multi-tenant transaction boundaries.
2. **Standalone Dummy Audit Routes:**
   - Isolated mock audit endpoints that only logged audit records without performing actual inventory or billing actions were removed. Audit logging is now wired directly into live business service mutations.
3. **Hardcoded Database Seed Credentials:**
   - Hardcoded database passwords and static demo credentials were removed in favor of 12-Factor `.env` configuration.

---

## 14. Local Development Setup

### 1. Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis Server 7.x
- MinIO or AWS S3 (for document/prescription storage)

### 2. Environment Setup
```bash
# Clone the repository
git clone <repository_url>
cd Medorax-Backend/medorax-erp-backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database & Environment Configuration
```bash
# Copy template environment file
cp .env.example .env

# Edit .env with your local PostgreSQL and Redis credentials
nano .env

# Run database migrations
alembic upgrade head
```

### 4. Starting Backend Services
Open separate terminal tabs for each service:

```bash
# Terminal 1: Start FastAPI Application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start Redis Server (if not running as a system service)
redis-server

# Terminal 3: Start Celery Worker
celery -A app.core.celery_app.celery_app worker --loglevel=info

# Terminal 4: Start Celery Beat Scheduler
celery -A app.core.celery_app.celery_app beat --loglevel=info
```

### 5. Interactive API Documentation
Once running, open in your browser:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI Schema:** `http://localhost:8000/openapi.json`

---

## 15. Environment Configuration Reference

The application loads configuration strictly via `app/core/config.py` using `pydantic-settings`. Never commit `.env` files containing production credentials.

| Variable | Type | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | String | *Required* | PostgreSQL connection string (`postgresql+psycopg://user:pass@host:5432/dbname`) |
| `JWT_SECRET` | String | *Required* | Cryptographic secret for signing JWTs (Minimum 32 characters) |
| `JWT_ALGORITHM` | String | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Integer | `15` | Expiry duration for access tokens |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Integer | `30` | Expiry duration for refresh tokens |
| `REDIS_URL` | String | `redis://localhost:6379/0` | Redis broker URL |
| `CELERY_BROKER_URL` | String | `redis://localhost:6379/0` | Celery broker URL |
| `CELERY_RESULT_BACKEND` | String | `redis://localhost:6379/1` | Celery result backend |
| `STORAGE_ENDPOINT` | String | `http://localhost:9000` | S3 / MinIO endpoint URL |
| `STORAGE_ACCESS_KEY` | String | *Required* | Storage access key ID |
| `STORAGE_SECRET_KEY` | String | *Required* | Storage secret access key |
| `STORAGE_BUCKET_PRESCRIPTIONS`| String | `prescriptions` | Bucket name for prescription scans |
| `STORAGE_BUCKET_DOCUMENTS` | String | `documents` | Bucket name for compliance certificates |
| `LLM_API_KEY` | String | None | OpenAI / Gemini API key for prescription parsing |
| `LLM_BASE_URL` | String | None | Custom base URL for LLM provider (optional) |
| `LLM_MODEL` | String | `qwen-plus` | LLM model identifier |

---

## 16. Remaining Work & Technical Roadmap

### 1. Integration Work in Progress
- Finalizing integration edge cases for complex multi-party invoice returns and partial credit notes.
- Harmonizing pharmacy profile image upload directly with S3 document storage.

### 2. Backend Fixes & Enhancements
- Fine-tuning database connection pool limits under high-concurrency point-of-sale spikes.
- Adding database indexes on historical `inventory_ledger.created_at` ranges for ultra-fast annual reporting.

### 3. Business Logic Validation
- Multi-threaded load testing for pessimistic `.with_for_update()` locking under simultaneous checkout race conditions.
- Validating Segregation of Duties (SoD) edge cases across multi-branch role hierarchies.

### 4. Frontend Readiness Milestones
- Developing frontend UI mockups strictly against endpoints marked **`✅ READY FOR FRONTEND`**.
- Coordinating API contract reviews for the Point-of-Sale (POS) and Prescription Review screens before marking them ready for end-to-end integration.

---
