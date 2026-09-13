"""
app/shared/middleware.py

Request ID middleware.

Assigns a unique UUID to every HTTP request and:
  1. Exposes it as X-Request-ID in the response header.
  2. Stores it in a ContextVar so it can be read by audit_log() and any
     logger throughout the lifetime of that request — without passing it
     through every function signature.

This is the prerequisite for distributed tracing: every log line emitted
during a request will share the same request_id, making it trivial to
reconstruct the full call chain in a log aggregator (Loki, Splunk, etc.).

If the client sends X-Request-ID (e.g., a mobile app with its own trace ID),
that value is preserved instead of generating a new one. This enables end-
to-end request correlation across client and server logs.
"""

import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.services.audit import request_id_var


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Attach a unique request ID to every request/response cycle.

    Priority:
      1. Use the X-Request-ID header if provided by the client.
      2. Otherwise generate a new UUID4.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        # Honour client-supplied trace IDs (mobile apps, API gateways, etc.)
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

        # Store in ContextVar — accessible by audit_log() without arg passing.
        token = request_id_var.set(request_id)
        try:
            response: Response = await call_next(request)
        finally:
            # Always restore the ContextVar, even on exception.
            request_id_var.reset(token)

        response.headers["X-Request-ID"] = request_id
        return response
