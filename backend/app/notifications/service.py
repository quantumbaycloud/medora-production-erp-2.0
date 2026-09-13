from sqlalchemy.orm import Session
from app.notifications.models import Notification
from app.notifications.schemas import NotificationCreate
from app.core.exceptions import NotFoundException

class NotificationService:

    @staticmethod
    def create_notification(
        db: Session,
        pharmacy_id: str,
        data: NotificationCreate
    ) -> Notification:
        notif = Notification(
            pharmacy_id=pharmacy_id,
            branch_id=data.branch_id,
            user_id=data.user_id,
            title=data.title,
            message=data.message,
            alert_type=data.alert_type,
            severity=data.severity,
            is_read=False,
        )
        db.add(notif)
        db.flush()
        return notif

    @staticmethod
    def list_notifications(
        db: Session,
        pharmacy_id: str,
        unread_only: bool = False,
        limit: int = 50,
    ) -> list[Notification]:
        q = db.query(Notification).filter(Notification.pharmacy_id == pharmacy_id)
        if unread_only:
            q = q.filter(Notification.is_read == False)
        return q.order_by(Notification.created_at.desc()).limit(limit).all()

    @staticmethod
    def mark_as_read(db: Session, pharmacy_id: str, notification_id: str) -> Notification:
        notif = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.pharmacy_id == pharmacy_id
        ).first()
        if not notif:
            raise NotFoundException("Notification")
        notif.is_read = True
        db.flush()
        return notif

    @staticmethod
    def mark_all_as_read(db: Session, pharmacy_id: str) -> int:
        count = db.query(Notification).filter(
            Notification.pharmacy_id == pharmacy_id,
            Notification.is_read == False
        ).update({"is_read": True})
        db.flush()
        return count
