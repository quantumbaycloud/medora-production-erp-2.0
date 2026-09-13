"""
app/core/logging_config.py

Logging configuration for the Medorax API.

Development: human-readable text to stdout.
Production:  JSON lines to stdout (parsed by log aggregators).

The "medorax.audit" logger is configured with its own handler to ensure
audit events are never dropped by a parent logger's level filter.

Usage:
    Call configure_logging() once in app startup (lifespan in main.py).
    After that, all loggers in the app emit structured JSON in production.

Example audit event (JSON, production):
    {
      "timestamp": "2026-07-15T10:00:00Z",
      "level": "INFO",
      "logger": "medorax.audit",
      "message": "LOGIN_SUCCESS",
      "event": "LOGIN_SUCCESS",
      "request_id": "a1b2c3d4",
      "user_id": "uuid...",
      "device_id": "uuid...",
      "ip_address": "1.2.3.4"
    }
"""

import logging
import logging.config
import os


def configure_logging() -> None:
    """
    Configure application logging.

    In production (LOG_FORMAT=json), uses python-json-logger to emit
    structured JSON. In development (default), uses a readable text format.

    python-json-logger is optional — if not installed, falls back to text.
    """
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_format = os.getenv("LOG_FORMAT", "text").lower()  # "text" | "json"

    if log_format == "json":
        try:
            from pythonjsonlogger import jsonlogger  # type: ignore[import]

            formatter = jsonlogger.JsonFormatter(
                fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%SZ",
                rename_fields={"asctime": "timestamp", "levelname": "level", "name": "logger"},
            )
        except ImportError:
            # python-json-logger not installed — fall back to text.
            formatter = logging.Formatter(
                "%(asctime)s %(levelname)-8s %(name)s: %(message)s"
            )
    else:
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)-8s %(name)s: %(message)s"
        )

    # Root handler
    root_handler = logging.StreamHandler()
    root_handler.setFormatter(formatter)

    # Dedicated audit handler — same formatter, ensures audit events always emit.
    audit_handler = logging.StreamHandler()
    audit_handler.setFormatter(formatter)
    audit_handler.setLevel(logging.DEBUG)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers = [root_handler]

    # Audit logger — dedicated, propagate=False so it is never filtered by root.
    audit_logger = logging.getLogger("medorax.audit")
    audit_logger.setLevel(logging.DEBUG)
    audit_logger.handlers = [audit_handler]
    audit_logger.propagate = False  # Do not forward to root — audit has its own handler.

    # Silence noisy third-party loggers in production.
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
