from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base, new_uuid

class InventoryLedger(Base):
    __tablename__ = "inventory_ledger"

    id = Column(String, primary_key=True, default=new_uuid)
    pharmacy_id = Column(String, ForeignKey("pharmacies.id"), nullable=False, index=True)
    branch_id = Column(String, ForeignKey("branches.id"), nullable=True, index=True)
    medicine_id = Column(String, ForeignKey("medicines.id"), nullable=False, index=True)

    batch_number = Column(String, nullable=False, index=True)
    transaction_type = Column(String, nullable=False, index=True)  # SALE, RETURN, EXCHANGE, PURCHASE, ADJUSTMENT, EXPIRY
    quantity = Column(Integer, nullable=False)
    reference_id = Column(String, nullable=True, index=True)  # invoice number, purchase number, etc.
    notes = Column(String, nullable=True)

    created_by_user_id = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class OpeningStock(Base):
    __tablename__ = "opening_stock"

    id = Column(String, primary_key=True, default=new_uuid)
    pharmacy_id = Column(String, ForeignKey("pharmacies.id"), nullable=False, index=True)
    branch_id = Column(String, ForeignKey("branches.id"), nullable=True, index=True)
    medicine_id = Column(String, ForeignKey("medicines.id"), nullable=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    medicine_name = Column(String, nullable=False)
    sku = Column(String, nullable=False, unique=True, index=True)
    category = Column(String, nullable=False, index=True)
    opening_qty = Column(Integer, nullable=False, default=0)
    unit = Column(String, nullable=False, default="Units")
    location = Column(String, nullable=True)
    remarks = Column(String, nullable=True)
    period_start_date = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    pharmacy = relationship("Pharmacy")
    branch = relationship("Branch")
    medicine = relationship("Medicine")
    user = relationship("User")
    
