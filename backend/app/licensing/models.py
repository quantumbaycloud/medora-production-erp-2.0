from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.sql import func

from app.db.base import Base, new_uuid


class LicenseActivation(Base):
    """Device activation record owned by an ERP tenant/pharmacy."""

    __tablename__ = "license_activations"
    __table_args__ = (
        UniqueConstraint("license_id", "device_id", name="uq_license_activation_device"),
    )

    id = Column(String, primary_key=True, default=new_uuid)
    license_id = Column(String(128), nullable=False, index=True)
    tenant_id = Column(String(128), nullable=False, index=True)
    device_id = Column(String(255), nullable=False, index=True)
    device_name = Column(String(255), nullable=True)
    plan = Column(String(64), nullable=False)
    status = Column(String(32), nullable=False, default="active", index=True)
    max_devices = Column(Integer, nullable=False, default=1)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    modules_json = Column(Text, nullable=False, default="[]")
    license_payload_json = Column(Text, nullable=False)
    last_validated_at = Column(DateTime(timezone=True), nullable=True)
    last_heartbeat_at = Column(DateTime(timezone=True), nullable=True)
    issuer_status = Column(String(32), nullable=True)
    revoked = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
