import uuid
from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.db.base import Base, new_uuid

class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, default=new_uuid)
    pharmacy_id = Column(String(100), nullable=False, index=True)
    customer_name = Column(String(255), nullable=True)
    name = Column(String(200), index=True, nullable=False)
    type = Column(String(50), index=True, default="Regular")  # Regular, Repeat, One-Time, VIP, New
    mobile_number = Column(String(50), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(String(500), nullable=True)
    gst_number = Column(String(50), nullable=True)
    notes = Column(String(1000), nullable=True)
    outstanding_amount = Column(Float, nullable=True, default=0.0)
    status = Column(String(20), nullable=True, default="Active")
    orders = Column(Integer, default=0, nullable=False)
    spend = Column(Float, default=0.0, nullable=False)
    last_purchase = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())