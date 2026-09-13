"""
app/main.py

FastAPI application entry point.

Startup sequence:
  1. configure_logging() — set up structured logging (JSON in production).
  2. Create FastAPI app with full OpenAPI metadata.
  3. Register middleware:
       - RequestIDMiddleware: X-Request-ID on every request/response.
  4. Register exception handlers:
       - RateLimitExceeded: 429 with Retry-After header (from slowapi).
  5. Include routers.
  6. Instrument with Prometheus (optional — skips gracefully if not installed).

Deployment:
  gunicorn -k uvicorn.workers.UvicornWorker -w 4 app.main:app

Metrics:
  GET /metrics — Prometheus scrape endpoint (add to Prometheus scrape config).
  In production, protect this endpoint behind a network ACL or a reverse
  proxy that only allows the Prometheus server's IP.
"""

import os
from dotenv import load_dotenv
load_dotenv()  

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.auth.router import internal_router, router as auth_router
from app.branch.router import router as branch_router
from app.core.logging_config import configure_logging

from app.pharmacy.router import router as pharmacy_router
from app.shared.middleware import RequestIDMiddleware
from app.shared.rate_limit import limiter
from app.user.router import router as user_router
from app.staff.router import router as staff_router
from app.medicine.router import router as medicine_router
from app.supplier.router import router as supplier_router
from app.purchase.router import router as purchase_router
from app.inventory.router import router as inventory_router
from app.customer.router import router as customer_router
from app.billing.router import router as billing_router
from app.audit.router import router as audit_router
from app.notifications.router import router as notifications_router
from app.reports.router import router as reports_router
from app.settings.router import router as settings_router
from app.prescription.router import router as prescription_router
from app.licensing.router import router as licensing_router
from app.provisioning.router import router as provisioning_router
from app.catalog.router import router as catalog_router
from app.admin_sync.router import router as admin_sync_router

from fastapi import Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session as DbSession
from app.db.base import get_db


# Configure structured logging before anything else.
configure_logging()
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler. Runs startup/shutdown logic."""
    # Startup: ensure tables exist and seed system roles and permissions
    from app.db.base import Base, engine, SessionLocal
    import app.auth.models  # noqa: F401
    import app.staff.models  # noqa: F401
    import app.supplier.models  # noqa: F401
    import app.customer.models  # noqa: F401
    import app.licensing.models  # noqa: F401
    import app.provisioning.models  # noqa: F401\n    import app.catalog.models  # noqa: F401

    # Local bootstrap can create tables. Production deployments should run
    # Alembic migrations explicitly and set AUTO_CREATE_TABLES=false.
    if settings.auto_create_tables:
        from sqlalchemy import text as sql_text
        with engine.begin() as connection:
            if engine.dialect.name == "postgresql":
                connection.execute(sql_text("SELECT pg_advisory_lock(68455321)"))
                try:
                    Base.metadata.create_all(bind=connection)
                finally:
                    connection.execute(sql_text("SELECT pg_advisory_unlock(68455321)"))
            else:
                Base.metadata.create_all(bind=connection)

    from app.staff.service import seed_system_roles_and_permissions
    with SessionLocal() as db:
        seed_system_roles_and_permissions(db)
    yield
    # Shutdown: connection pools close automatically.


app = FastAPI(
    title="Medorax API",
    description=(
        "Medorax backend API — pharmacy management and healthcare platform.\n\n"
        "## Authentication\n"
        "All protected endpoints require a Bearer token in the `Authorization` header:\n"
        "```\nAuthorization: Bearer <access_token>\n```\n\n"
        "## Token Rotation\n"
        "Refresh tokens rotate on every use (RTR). Replaying a used refresh token "
        "triggers a security event that revokes all sessions for that user.\n\n"
        "## Device Management\n"
        "The client must persist `device_identifier` from the login response "
        "and send it on subsequent logins to enforce one-session-per-device.\n\n"
        "## Rate Limiting\n"
        "Authentication endpoints are rate-limited per client IP. Exceeded limits "
        "return `429 Too Many Requests` with a `Retry-After` header."
    ),
    version="1.0.0",
    contact={
        "name": "Medorax Engineering",
        "email": "engineering@medorax.com",
    },
    license_info={
        "name": "Proprietary",
    },
    lifespan=lifespan,
)

# ── Rate Limiting ─────────────────────────────────────────────────────────────
# Attach slowapi limiter to app state and register the 429 exception handler.
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── Middleware ─────────────────────────────────────────────────────────────────
# Order matters: middleware is applied in reverse registration order (LIFO).
app.add_middleware(RequestIDMiddleware)

from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

origins = settings.cors_origins
if isinstance(origins, str):
    origins = [orig.strip() for orig in origins.split(",") if orig.strip()]
# Local commercial ERP is served by Vite on localhost; also accept 127.0.0.1
# so switching the browser host does not turn backend failures into CORS errors.
if settings.app_env != "production":
    origins = list(dict.fromkeys([*origins, "http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "http://127.0.0.1:3000"]))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(internal_router)
app.include_router(user_router)
app.include_router(pharmacy_router)
app.include_router(branch_router)
app.include_router(staff_router)
app.include_router(medicine_router)
app.include_router(supplier_router)
app.include_router(purchase_router)
app.include_router(inventory_router)
app.include_router(customer_router)
app.include_router(billing_router)
app.include_router(audit_router)
app.include_router(notifications_router)
app.include_router(reports_router)
app.include_router(settings_router)
app.include_router(prescription_router)
app.include_router(licensing_router)
app.include_router(provisioning_router)
app.include_router(catalog_router)
app.include_router(admin_sync_router)

logger = logging.getLogger("medorax")

# ── Prometheus Metrics ────────────────────────────────────────────────────────
# prometheus-fastapi-instrumentator instruments all endpoints automatically.
# Exposes GET /metrics in Prometheus text format.
# If the library is not installed, metrics are silently skipped (dev convenience).
try:
    from prometheus_fastapi_instrumentator import Instrumentator

    Instrumentator(
        should_group_status_codes=False,
        should_ignore_untemplated=True,
        should_respect_env_var=True,  # honours ENABLE_METRICS env var
        should_instrument_requests_inprogress=True,
        excluded_handlers=["/metrics"],
    ).instrument(app).expose(app, include_in_schema=False)
except ImportError:
    logger.warning(
        "prometheus-fastapi-instrumentator not installed — metrics endpoint disabled."
    )


# ── Health Check ──────────────────────────────────────────────────────────────
@app.get("/health/live", include_in_schema=False)
def live():
    return {"status": "alive"}



@app.get("/health/ready", summary="Readiness Check", tags=["ops"])
def ready(db: DbSession = Depends(get_db)):
    """Readiness endpoint verifying database connectivity."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception:
        logger.exception("Database readiness check failed")
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        )
