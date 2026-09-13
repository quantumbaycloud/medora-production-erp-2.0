from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import relationship
from app.db.base import Base, new_uuid

class CatalogOption(Base):
    __tablename__ = "catalog_options"
    __table_args__ = (UniqueConstraint("pharmacy_id", "option_type", "code", name="uq_catalog_pharmacy_type_code"),)

    id = Column(String, primary_key=True, default=new_uuid)
    pharmacy_id = Column(String, ForeignKey("pharmacies.id", ondelete="CASCADE"), nullable=False, index=True)
    option_type = Column(String(60), nullable=False, index=True)
    code = Column(String(80), nullable=False)
    name = Column(String(160), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    sort_order = Column(Integer, nullable=False, default=0)
    metadata_json = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    pharmacy = relationship("Pharmacy")
