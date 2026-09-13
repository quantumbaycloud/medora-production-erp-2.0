from sqlalchemy import Column, String, ForeignKey, Numeric, Integer, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base, new_uuid

class PharmacySetting(Base):
    __tablename__ = "pharmacy_settings"

    id = Column(String, primary_key=True, default=new_uuid)
    pharmacy_id = Column(String, ForeignKey("pharmacies.id"), unique=True, nullable=False, index=True)

    # ERP Configuration
    company_name = Column(String, nullable=True)
    default_gst_percentage = Column(Numeric(10, 2), default=18.00, nullable=False)
    invoice_template = Column(String, default="Standard Clean Layout", nullable=False)
    printer_settings = Column(String, default="Thermal 80mm", nullable=False)
    barcode_settings = Column(String, default="Code128", nullable=False)
    backup_settings = Column(String, default="Daily Auto-Backup", nullable=False)

    # Security & Compliance Configuration
    session_timeout_minutes = Column(Integer, default=30, nullable=False)
    maintenance_mode = Column(Boolean, default=False, nullable=False)
    audit_log_retention_days = Column(Integer, default=365, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    pharmacy = relationship("Pharmacy")
