"""
Health Check utility.

Aggregates individual component checks (database, disk, memory, CPU) into
one overall status: "healthy", "degraded", or "unhealthy".

- healthy:   all checks pass
- degraded:  non-critical checks (disk/memory/cpu) are past a warning
             threshold but the service is still usable
- unhealthy: a critical check (database) fails
"""
import shutil
import time
from datetime import datetime, timezone

import psutil
from sqlalchemy import text
from sqlalchemy.orm import Session

START_TIME = time.time()

DISK_WARN_PCT = 85
MEMORY_WARN_PCT = 85
CPU_WARN_PCT = 90


def check_database(db: Session) -> dict:
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as exc:  # pragma: no cover - defensive
        return {"status": "error", "detail": str(exc)}


def check_disk() -> dict:
    total, used, free = shutil.disk_usage("/")
    pct_used = round((used / total) * 100, 1)
    return {
        "status": "warn" if pct_used >= DISK_WARN_PCT else "ok",
        "percent_used": pct_used,
        "free_gb": round(free / (1024**3), 2),
    }


def check_memory() -> dict:
    mem = psutil.virtual_memory()
    return {
        "status": "warn" if mem.percent >= MEMORY_WARN_PCT else "ok",
        "percent_used": mem.percent,
        "available_mb": round(mem.available / (1024**2), 1),
    }


def check_cpu() -> dict:
    pct = psutil.cpu_percent(interval=0.2)
    return {"status": "warn" if pct >= CPU_WARN_PCT else "ok", "percent_used": pct}


def run_health_check(db: Session) -> dict:
    checks = {
        "database": check_database(db),
        "disk": check_disk(),
        "memory": check_memory(),
        "cpu": check_cpu(),
    }

    if checks["database"]["status"] == "error":
        overall = "unhealthy"
    elif any(c["status"] == "warn" for c in checks.values()):
        overall = "degraded"
    else:
        overall = "healthy"

    return {
        "status": overall,
        "timestamp": datetime.now(timezone.utc),
        "uptime_seconds": round(time.time() - START_TIME, 1),
        "checks": checks,
    }
