from datetime import date, timedelta
from app.core.celery_app import celery_app
from app.db.base import SessionLocal
from app.medicine.models import Medicine, MedicineBatch
from app.notifications.models import Notification
from app.pharmacy.models import Pharmacy

@celery_app.task(name="check_low_stock_and_expiry")
def check_low_stock_and_expiry_task():
    """
    Periodic Celery Beat task to scan all active pharmacies for low stock
    and near-expiry batches, generating in-app system notifications.
    """
    today = date.today()
    expiry_threshold = today + timedelta(days=30)

    with SessionLocal() as db:
        pharmacies = db.query(Pharmacy).all()

        for ph in pharmacies:
            # 1. Check Low Stock Batches
            low_stock_batches = (
                db.query(MedicineBatch, Medicine)
                .join(Medicine, Medicine.id == MedicineBatch.medicine_id)
                .filter(
                    Medicine.pharmacy_id == ph.id,
                    MedicineBatch.status == "ACTIVE",
                    MedicineBatch.quantity_available <= Medicine.min_stock_level
                )
                .all()
            )

            for batch, med in low_stock_batches:
                existing = db.query(Notification).filter(
                    Notification.pharmacy_id == ph.id,
                    Notification.alert_type == "LOW_STOCK",
                    Notification.message.like(f"%{med.name}%{batch.batch_number}%"),
                    Notification.is_read == False
                ).first()

                if not existing:
                    notif = Notification(
                        pharmacy_id=ph.id,
                        title=f"Low Stock Alert: {med.name}",
                        message=f"Medicine '{med.name}' (Batch: {batch.batch_number}) has only {batch.quantity_available} units remaining (Threshold: {med.min_stock_level}).",
                        alert_type="LOW_STOCK",
                        severity="WARNING",
                    )
                    db.add(notif)

            # 2. Check Near-Expiry Batches
            expiring_batches = (
                db.query(MedicineBatch, Medicine)
                .join(Medicine, Medicine.id == MedicineBatch.medicine_id)
                .filter(
                    Medicine.pharmacy_id == ph.id,
                    MedicineBatch.status == "ACTIVE",
                    MedicineBatch.expiry_date <= expiry_threshold
                )
                .all()
            )

            for batch, med in expiring_batches:
                is_expired = batch.expiry_date < today
                severity = "CRITICAL" if is_expired else "WARNING"
                alert_title = f"{'Expired' if is_expired else 'Near Expiry'} Alert: {med.name}"

                existing = db.query(Notification).filter(
                    Notification.pharmacy_id == ph.id,
                    Notification.alert_type == "EXPIRY",
                    Notification.message.like(f"%{med.name}%{batch.batch_number}%"),
                    Notification.is_read == False
                ).first()

                if not existing:
                    notif = Notification(
                        pharmacy_id=ph.id,
                        title=alert_title,
                        message=f"Medicine '{med.name}' (Batch: {batch.batch_number}) expires on {batch.expiry_date}. Current stock: {batch.quantity_available}.",
                        alert_type="EXPIRY",
                        severity=severity,
                    )
                    db.add(notif)

        db.commit()
    return "Check completed successfully"
