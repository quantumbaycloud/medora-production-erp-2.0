import logging
import sys

logger = logging.getLogger("financial_audit")
logger.setLevel(logging.INFO)

log_format = logging.Formatter(
    '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "module": "%(name)s", "message": "%(message)s"}'
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)