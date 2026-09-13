from sqlalchemy import Column, String, ForeignKey, Numeric, Integer, Date
from sqlalchemy.orm import relationship
from app.db.base import Base, new_uuid

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(String, primary_key=True, default=new_uuid)
    pharmacy_id = Column(String, ForeignKey("pharmacies.id"), nullable=False, index=True)

    name = Column(String, nullable=False, index=True)
    generic_name = Column(String, nullable=True)
    brand_name = Column(String, nullable=True)
    manufacturer = Column(String, nullable=True)
    category = Column(String, nullable=True)
    unit = Column(String, nullable=True)
    barcode = Column(String, nullable=True, unique=True, index=True)
    sku = Column(String, nullable=True, unique=True, index=True)
    schedule_type = Column(String, nullable=True)
    hsn_code = Column(String, nullable=True)
    gst_percentage = Column(Numeric(10, 2), nullable=True)
    min_stock_level = Column(Integer, default=0)
    rack = Column(String, nullable=True)

    # Relationships
    pharmacy = relationship("Pharmacy")
    batches = relationship("MedicineBatch", back_populates="medicine", cascade="all, delete-orphan")


class MedicineBatch(Base):
    __tablename__ = "medicine_batches"

    id = Column(String, primary_key=True, default=new_uuid)
    medicine_id = Column(String, ForeignKey("medicines.id"), nullable=False, index=True)
    
    batch_number = Column(String, nullable=False, index=True)
    expiry_date = Column(Date, nullable=False)
    purchase_price = Column(Numeric(10, 2), nullable=False)
    selling_price = Column(Numeric(10, 2), nullable=False)
    mrp = Column(Numeric(10, 2), nullable=False)
    quantity_available = Column(Integer, default=0, nullable=False)
    status = Column(String, default="ACTIVE", nullable=False) # ACTIVE, EXPIRED, QUARANTINED

    # Relationships
    medicine = relationship("Medicine", back_populates="batches")
