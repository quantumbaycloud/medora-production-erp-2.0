from sqlalchemy.orm import Session
from app.settings.models import PharmacySetting
from app.settings.schemas import SettingUpdate
from app.audit.service import AuditService

class SettingService:

    @staticmethod
    def get_or_create_settings(db: Session, pharmacy_id: str) -> PharmacySetting:
        setting = db.query(PharmacySetting).filter(PharmacySetting.pharmacy_id == pharmacy_id).first()
        if not setting:
            setting = PharmacySetting(pharmacy_id=pharmacy_id)
            db.add(setting)
            db.flush()
        return setting

    @staticmethod
    def update_settings(
        db: Session,
        pharmacy_id: str,
        user_id: str,
        user_email: str,
        data: SettingUpdate,
        ip_address: str = None
    ) -> PharmacySetting:
        setting = SettingService.get_or_create_settings(db, pharmacy_id)
        update_dict = data.model_dump(exclude_unset=True)

        for key, value in update_dict.items():
            setattr(setting, key, value)

        db.flush()

        # Audit trail
        AuditService.log(
            db=db,
            pharmacy_id=pharmacy_id,
            user_id=user_id,
            user_email=user_email,
            action_type="SETTINGS_CHANGE",
            category="Settings",
            entity_type="PharmacySetting",
            entity_id=setting.id,
            ip_address=ip_address,
            details={k: str(v) for k, v in update_dict.items()},
        )

        return setting
