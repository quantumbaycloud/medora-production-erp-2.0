from sqlalchemy import Column, String, ForeignKey, Boolean, DateTime, Text, func
from sqlalchemy.orm import relationship
from app.db.base import Base, new_uuid

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, default=new_uuid)
    pharmacy_id = Column(String, ForeignKey("pharmacies.id"), nullable=False, index=True)
    branch_id = Column(String, ForeignKey("branches.id"), nullable=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)

    title = Column(String(150), nullable=False)
    message = Column(Text, nullable=False)
    alert_type = Column(String(50), nullable=False, index=True)  # LOW_STOCK, EXPIRY, PURCHASE_APPROVED, SYSTEM
    severity = Column(String(20), default="INFO", nullable=False)  # INFO, WARNING, CRITICAL
    is_read = Column(Boolean, default=False, nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    pharmacy = relationship("Pharmacy")
    branch = relationship("Branch")
    user = relationship("User")
