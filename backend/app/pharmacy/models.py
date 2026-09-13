"""
Pharmacy = business profile + ownership. Depends on `user` ownership
membership, per the module dependency chain: Auth -> User -> Pharmacy ->
Branch -> Staff.

Per the File Management discussion: `logo` stays here (it's a profile
attribute, not a compliance document). GST certificate, drug license, and
PAN are stored as `document_id` references -- the actual files/documents
live in Intern D's Document Management module, not here. This module never
stores a raw file path/URL for those three; it only stores the reference.
"""
from sqlalchemy import Column, DateTime, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base, new_uuid


class Pharmacy(Base):
    __tablename__ = "pharmacies"

    id = Column(String, primary_key=True, default=new_uuid)

    # Original/primary owner retained for existing API responses.
    # Authorization uses PharmacyOwner memberships below.
    owner_user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    # --- Business information ---
    name = Column(String, nullable=False)
    logo_path = Column(String, nullable=True)  # profile image, stored directly here

    gst_number = Column(String, unique=True, nullable=True, index=True)

    # References into Intern D's Document Management module.
    # This module does not know or care about file storage details.
    drug_license_document_id = Column(String, nullable=True)
    gst_certificate_document_id = Column(String, nullable=True)
    pan_document_id = Column(String, nullable=True)

    pan_number = Column(String, nullable=True)

    address = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)

    bank_account_number = Column(String, nullable=True)
    bank_ifsc = Column(String, nullable=True)
    bank_name = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # ORM Relationships
    owner = relationship("User", foreign_keys=[owner_user_id], back_populates="pharmacies")
    owners = relationship("PharmacyOwner", back_populates="pharmacy", cascade="all, delete-orphan")
    branches = relationship("Branch", back_populates="pharmacy", cascade="all, delete-orphan")


class PharmacyOwner(Base):
    __tablename__ = "pharmacy_owners"
    __table_args__ = (PrimaryKeyConstraint("pharmacy_id", "user_id"),)

    pharmacy_id = Column(String, ForeignKey("pharmacies.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # ORM Relationships
    pharmacy = relationship("Pharmacy", back_populates="owners")
    user = relationship("User")
