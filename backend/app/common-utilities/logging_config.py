"""
Central logging configuration.

Sets up three rotating, JSON-formatted log files on disk (in addition to the
DB tables in models.py) so logs survive even if the database is unreachable:

- logs/error.log     -> ERROR and above
- logs/activity.log  -> user/API activity
- logs/system.log    -> INFO and above, general system events

Each file rotates at 5MB, keeping 5 backups, to prevent unbounded growth.
"""
import json
import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

MAX_BYTES = 5 * 1024 * 1024  # 5MB
BACKUP_COUNT = 5


class JsonFormatter(logging.Formatter):
    """Formats log records as single-line JSON for easy parsing/ingestion."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        # Allow arbitrary structured extras (e.g. user_id, action) to be merged in
        for key, value in getattr(record, "extra_fields", {}).items():
            payload[key] = value
        return json.dumps(payload)


def _build_logger(name: str, filename: str, level: int) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # avoid duplicate logs via the root logger

    if not logger.handlers:  # guard against re-adding handlers on reload
        file_handler = RotatingFileHandler(
            os.path.join(LOG_DIR, filename), maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT
        )
        file_handler.setFormatter(JsonFormatter())
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        logger.addHandler(console_handler)

    return logger


error_logger = _build_logger("error_logger", "error.log", logging.ERROR)
activity_logger = _build_logger("activity_logger", "activity.log", logging.INFO)
system_logger = _build_logger("system_logger", "system.log", logging.DEBUG)


def log_with_extra(logger: logging.Logger, level: int, message: str, **extra_fields):
    """Log a message while attaching structured extra fields for the JSON formatter."""
    logger.log(level, message, extra={"extra_fields": extra_fields})
