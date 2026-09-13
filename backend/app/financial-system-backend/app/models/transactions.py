from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone
import enum

Base = declarative_base()

from app.database.base_class import TransactionType

class CashTransaction(Base):
    __tablename__ = "cash_transactions"  # Fixed typo here
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    source = Column(String, nullable=False)
    remarks = Column(String, nullable=True)
    # Added timezone=True and renamed to created_at
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(String, primary_key=True) # Gateway generated Order ID
    gateway = Column(String, nullable=False) # "razorpay", "paytm", etc.
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String, default="created") # created, paid, failed
    # Added timezone=True
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class BankTransaction(Base):
    __tablename__ = "bank_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, ForeignKey("orders.id"), nullable=True)
    gateway_transaction_id = Column(String, unique=True, nullable=False) # Ensures idempotency
    amount = Column(Numeric(10, 2), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    # Added timezone=True
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))