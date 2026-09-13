"""
ActivityLoggingMiddleware

Automatically records one ActivityLog row (+ file log entry) per incoming
HTTP request: method, path, status code, client IP, and duration. Attach a
`request.state.user_id` upstream (e.g. in an auth dependency) and it will be
captured automatically.
"""
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from database import SessionLocal
from models import ActivityLog
from logging_config import activity_logger, log_with_extra
import logging

# Endpoints we don't want cluttering the activity log
EXCLUDED_PATHS = {"/health", "/docs", "/openapi.json", "/redoc"}


class ActivityLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration_ms = round((time.time() - start) * 1000, 1)

        if request.url.path not in EXCLUDED_PATHS:
            user_id = getattr(request.state, "user_id", None)
            status = "SUCCESS" if response.status_code < 400 else "FAILURE"

            log_with_extra(
                activity_logger,
                logging.INFO,
                f"{request.method} {request.url.path} -> {response.status_code}",
                user_id=user_id,
                status_code=response.status_code,
                duration_ms=duration_ms,
                ip=request.client.host if request.client else None,
            )

            db = SessionLocal()
            try:
                db.add(ActivityLog(
                    user_id=user_id,
                    action=f"{request.method} {request.url.path}",
                    resource=request.url.path,
                    ip_address=request.client.host if request.client else None,
                    status=status,
                    details=f"status_code={response.status_code}, duration_ms={duration_ms}",
                ))
                db.commit()
            except Exception:
                db.rollback()  # never let logging break the actual request
            finally:
                db.close()

        return response
