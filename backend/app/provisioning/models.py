from sqlalchemy import Column, DateTime, String, Text, UniqueConstraint
from sqlalchemy.sql import func

from app.db.base import Base, new_uuid


class ProvisionedLicense(Base):
    """Tenant-level signed license installed by onboarding."""

    __tablename__ = "provisioned_licenses"
    __table_args__ = (UniqueConstraint("tenant_id", name="uq_provisioned_license_tenant"),)

    id = Column(String, primary_key=True, default=new_uuid)
    tenant_id = Column(String(128), nullable=False, index=True)
    license_id = Column(String(128), nullable=False, unique=True, index=True)
    plan = Column(String(64), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    license_json = Column(Text, nullable=False)
    signature = Column(Text, nullable=False)
    status = Column(String(32), nullable=False, default="active", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
