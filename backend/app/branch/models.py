"""
Branch belongs to exactly one Pharmacy. Sits between Pharmacy and Staff in
the dependency chain (Auth -> User -> Pharmacy -> Branch -> Staff).
"""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base, new_uuid

# TODO(founder): fixed set for now (Active/Inactive) -- confirm whether a
# "Closed" or "Suspended" status is also needed (Section 25: "Delete
# branch?" implies soft-delete via status rather than hard delete may be
# the intended pattern).
BRANCH_STATUSES = ("active", "inactive")


class Branch(Base):
    __tablename__ = "branches"

    id = Column(String, primary_key=True, default=new_uuid)
    pharmacy_id = Column(String, ForeignKey("pharmacies.id"), nullable=False, index=True)

    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)

    # TODO(founder): should branch-level settings (e.g. operating hours,
    # timezone) live as columns here, or as a separate `branch_settings`
    # key-value table for flexibility? Kept as a single JSON-ish string
    # placeholder for now -- revisit once the actual settings list exists.
    settings_json = Column(String, nullable=True)

    status = Column(String, default="active", nullable=False)  # one of BRANCH_STATUSES
    is_active = Column(Boolean, default=True, nullable=False)  # soft-delete flag

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # ORM Relationships
    pharmacy = relationship("Pharmacy", back_populates="branches")
