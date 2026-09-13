"""
app/services/audit.py

Structured security event audit logger.

Design:
  - Uses a dedicated "medorax.audit" logger, separate from the application
    logger. This allows routing audit events to a different sink (e.g., a
    SIEM, a separate log file, or a log aggregator filter) in production.
  - Each event is emitted as a single log record with structured `extra` fields.
    In production (with python-json-logger configured), each call to audit_log()
    produces one JSON line that is queryable by event type, user, device, etc.
  - request_id is propagated via a ContextVar populated by RequestIDMiddleware.
    It threads the same ID through all log records for a single HTTP request,
    enabling distributed trace reconstruction.

Usage:
    from app.services.audit import audit_log
    audit_log("LOGIN_SUCCESS", user_id=user.id, device_id=device.id, ip_address=ip)

Events (expand as needed):
    USER_REGISTERED, EMAIL_VERIFIED,
    LOGIN_SUCCESS, LOGIN_FAILED,
    TOKEN_ROTATED, ROTATION_BREACH,
    SESSION_CREATED, SESSION_REVOKED, SESSION_REPLACED,
    DEVICE_ADDED, DEVICE_REACTIVATED, DEVICE_DEACTIVATED,
    PASSWORD_RESET_REQUESTED, PASSWORD_RESET_COMPLETED,
    EMAIL_SENT, EMAIL_FAILED
"""

import contextvars
import logging
from datetime import datetime, timezone
from typing import Any

# Separate logger — configure this independently of app logger in production.
# In development it falls through to the root handler (readable text).
# In production configure it with python-json-logger to emit JSON lines.
_audit_logger = logging.getLogger("medorax.audit")

# Thread-local (actually async-local) request ID, set by RequestIDMiddleware.
request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default="-"
)


_LOGRECORD_RESERVED = {
    "name",
    "msg",
    "args",
    "exc_info",
    "func",
    "sinfo",
    "level",
    "levelname",
    "pathname",
    "filename",
    "module",
    "lineno",
    "created",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "process",
    "processName",
    "message",
    "asctime",
    "taskName",
}


def audit_log(event: str, **kwargs: Any) -> None:
    """
    Emit a structured security audit event.

    Args:
        event: The event name (e.g., "LOGIN_SUCCESS").
        **kwargs: Arbitrary structured fields (user_id, device_id, ip_address, etc.).
                  All fields are serialised into the log record's `extra` dict.

    Example output (JSON, production):
        {
          "timestamp": "2026-07-15T10:00:00Z",
          "level": "INFO",
          "logger": "medorax.audit",
          "event": "LOGIN_SUCCESS",
          "request_id": "abc123",
          "user_id": "uuid...",
          "device_id": "uuid...",
          "ip_address": "1.2.3.4"
        }
    """
    safe_kwargs = {}
    for k, v in kwargs.items():
        if k in _LOGRECORD_RESERVED:
            safe_kwargs[f"event_{k}"] = v
        else:
            safe_kwargs[k] = v

    _audit_logger.info(
        event,
        extra={
            "event": event,
            "request_id": request_id_var.get(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **safe_kwargs,
        },
    )
