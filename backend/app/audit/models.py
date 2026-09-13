from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, JSON, func
from sqlalchemy.orm import relationship
from app.db.base import Base, new_uuid

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=new_uuid)
    pharmacy_id = Column(String, ForeignKey("pharmacies.id"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    user_email = Column(String, nullable=True)

    action_type = Column(String, nullable=False, index=True)  # LOGIN, SALE, RETURN, EXCHANGE, PURCHASE, STOCK_CHANGE, etc.
    category = Column(String, nullable=True, index=True)      # Auth, Inventory, Billing, Purchase, Documents, Settings
    entity_type = Column(String, nullable=True)               # Invoice, Medicine, Supplier, Document, Staff
    entity_id = Column(String, nullable=True, index=True)
    ip_address = Column(String, nullable=True)
    details = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    pharmacy = relationship("Pharmacy")
    user = relationship("User")


class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    id = Column(String, primary_key=True, default=new_uuid)
    pharmacy_id = Column(String, ForeignKey("pharmacies.id"), nullable=False, index=True)

    category = Column(String(100), nullable=False, index=True)  # Drug License, GST Certificate, Purchase Bills, Supplier Documents, Staff Documents, Prescriptions, Other
    title = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_key = Column(String(500), nullable=False)
    mime_type = Column(String(100), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)

    entity_id = Column(String(100), nullable=True, index=True)
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    uploaded_by_user_id = Column(String, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    pharmacy = relationship("Pharmacy")
    uploader = relationship("User")
