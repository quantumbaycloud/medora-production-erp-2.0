from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "medorax_erp",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "app.reports.tasks",
        "app.prescription.tasks",
    ]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)

# Celery Beat schedule:
celery_app.conf.beat_schedule = {
    "daily_stock_and_expiry_check": {
        "task": "check_low_stock_and_expiry",
        "schedule": 86400.0,  # Every 24 hours
    },
}
