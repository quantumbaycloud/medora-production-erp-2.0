from sqlalchemy import Column, String, ForeignKey, Numeric, Integer, DateTime, Text, func
from sqlalchemy.orm import relationship
from app.db.base import Base, new_uuid

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(String, primary_key=True, default=new_uuid)
    pharmacy_id = Column(String, ForeignKey("pharmacies.id"), nullable=False, index=True)
    branch_id = Column(String, ForeignKey("branches.id"), nullable=True, index=True)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=True, index=True)

    invoice_number = Column(String(50), unique=True, nullable=False, index=True)
    invoice_date = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    customer_name = Column(String(200), nullable=True)

    total_amount = Column(Numeric(10, 2), nullable=False)
    discount_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    tax_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    payment_method = Column(String(50), nullable=False)
    payment_status = Column(String(30), nullable=False)  # Paid, Pending, Partially Paid

    cash_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    card_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    upi_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    wallet_amount = Column(Numeric(10, 2), default=0.00, nullable=False)

    created_by_user_id = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    pharmacy = relationship("Pharmacy")
    branch = relationship("Branch")
    customer = relationship("Customer")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(String, primary_key=True, default=new_uuid)
    invoice_id = Column(String, ForeignKey("invoices.id"), nullable=False, index=True)
    medicine_id = Column(String, ForeignKey("medicines.id"), nullable=False, index=True)
    batch_id = Column(String, ForeignKey("medicine_batches.id"), nullable=True, index=True)

    medicine_name = Column(String(200), nullable=False)
    batch_number = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    rate = Column(Numeric(10, 2), nullable=False)
    discount = Column(Numeric(10, 2), default=0.00, nullable=False)
    gst_percentage = Column(Numeric(10, 2), default=0.00, nullable=False)
    gst_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)

    # Relationships
    invoice = relationship("Invoice", back_populates="items")
    medicine = relationship("Medicine")
    batch = relationship("MedicineBatch")


class HoldBill(Base):
    __tablename__ = "hold_bills"

    id = Column(String, primary_key=True, default=new_uuid)
    pharmacy_id = Column(String, ForeignKey("pharmacies.id"), nullable=False, index=True)
    branch_id = Column(String, ForeignKey("branches.id"), nullable=True, index=True)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=True)

    hold_number = Column(String(100), unique=True, nullable=False, index=True)
    customer_name = Column(String(200), nullable=True)
    items_json = Column(Text, nullable=False)  # JSON-encoded array of items
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default="HOLD", nullable=False)  # HOLD, RESUMED, CANCELLED

    created_by_user_id = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ReturnBill(Base):
    __tablename__ = "return_bills"

    id = Column(String, primary_key=True, default=new_uuid)
    pharmacy_id = Column(String, ForeignKey("pharmacies.id"), nullable=False, index=True)
    branch_id = Column(String, ForeignKey("branches.id"), nullable=True, index=True)
    invoice_id = Column(String, ForeignKey("invoices.id"), nullable=True, index=True)

    invoice_number = Column(String(100), nullable=False, index=True)
    medicine_id = Column(String, ForeignKey("medicines.id"), nullable=False)
    medicine_name = Column(String(255), nullable=False)
    batch_number = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    refund_amount = Column(Numeric(10, 2), nullable=False)
    reason = Column(String(255), nullable=True)

    created_by_user_id = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ExchangeBill(Base):
    __tablename__ = "exchange_bills"

    id = Column(String, primary_key=True, default=new_uuid)
    pharmacy_id = Column(String, ForeignKey("pharmacies.id"), nullable=False, index=True)
    branch_id = Column(String, ForeignKey("branches.id"), nullable=True, index=True)
    invoice_id = Column(String, ForeignKey("invoices.id"), nullable=True, index=True)

    invoice_number = Column(String(100), nullable=False, index=True)

    old_medicine_id = Column(String, ForeignKey("medicines.id"), nullable=False)
    old_medicine_name = Column(String(255), nullable=False)
    old_batch_number = Column(String(100), nullable=False)
    old_quantity = Column(Integer, nullable=False)

    new_medicine_id = Column(String, ForeignKey("medicines.id"), nullable=False)
    new_medicine_name = Column(String(255), nullable=False)
    new_batch_number = Column(String(100), nullable=False)
    new_quantity = Column(Integer, nullable=False)

    price_difference = Column(Numeric(10, 2), default=0.00, nullable=False)

    created_by_user_id = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
