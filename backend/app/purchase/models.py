from sqlalchemy import Column, String, ForeignKey, DateTime, Date, Numeric, Boolean, Integer, func
from sqlalchemy.orm import relationship
from app.db.base import Base, new_uuid

class PurchaseInvoice(Base):
    __tablename__ = "purchase_invoices"

    id = Column(String, primary_key=True, default=new_uuid)
    pharmacy_id = Column(String, ForeignKey("pharmacies.id"), nullable=False, index=True)
    branch_id = Column(String, ForeignKey("branches.id"), nullable=True, index=True)
    supplier_id = Column(String, ForeignKey("suppliers.id"), nullable=False, index=True)

    invoice_number = Column(String, nullable=False, index=True)
    invoice_date = Column(Date, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    paid_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    is_paid = Column(Boolean, default=False, nullable=False)
    status = Column(String, default="DRAFT", nullable=False)  # DRAFT, APPROVED, RECEIVED, CANCELLED
    notes = Column(String, nullable=True)

    created_by_user_id = Column(String, ForeignKey("users.id"), nullable=True)
    approved_by_user_id = Column(String, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    pharmacy = relationship("Pharmacy")
    branch = relationship("Branch")
    supplier = relationship("Supplier", back_populates="purchases")
    items = relationship("PurchaseItem", back_populates="purchase", cascade="all, delete-orphan")


class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    id = Column(String, primary_key=True, default=new_uuid)
    purchase_id = Column(String, ForeignKey("purchase_invoices.id"), nullable=False, index=True)
    medicine_id = Column(String, ForeignKey("medicines.id"), nullable=False, index=True)

    batch_number = Column(String, nullable=False)
    expiry_date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    free_quantity = Column(Integer, default=0, nullable=False)
    purchase_price = Column(Numeric(10, 2), nullable=False)
    mrp = Column(Numeric(10, 2), nullable=False)
    selling_price = Column(Numeric(10, 2), nullable=False)
    tax_percentage = Column(Numeric(10, 2), default=0.00, nullable=False)
    discount_percentage = Column(Numeric(10, 2), default=0.00, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)

    # Relationships
    purchase = relationship("PurchaseInvoice", back_populates="items")
    medicine = relationship("Medicine")
