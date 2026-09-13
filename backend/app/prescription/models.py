from sqlalchemy import Column, String, ForeignKey, DateTime, Text, JSON, func
from sqlalchemy.orm import relationship
from app.db.base import Base, new_uuid

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(String, primary_key=True, default=new_uuid)
    pharmacy_id = Column(String, ForeignKey("pharmacies.id"), nullable=False, index=True)
    branch_id = Column(String, ForeignKey("branches.id"), nullable=True, index=True)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=True, index=True)

    file_name = Column(String(255), nullable=False)
    file_key = Column(String(500), nullable=False)
    extracted_text = Column(Text, nullable=True)
    analysis_result = Column(JSON, nullable=True)

    status = Column(String(30), default="UPLOADED", nullable=False)  # UPLOADED, PROCESSING, COMPLETED, REVIEWED, FAILED
    reviewed_by_user_id = Column(String, ForeignKey("users.id"), nullable=True)
    reviewer_notes = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    pharmacy = relationship("Pharmacy")
    branch = relationship("Branch")
    customer = relationship("Customer")
    reviewer = relationship("User")
