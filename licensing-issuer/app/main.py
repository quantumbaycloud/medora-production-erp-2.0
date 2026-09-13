import base64
import json
import os
import secrets
import time
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import Boolean, DateTime, Integer, String, Text, UniqueConstraint, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.sql import func

APP = FastAPI(title="MEDORAX Licensing Issuer", version="2.0.0", docs_url="/docs")
KEY_DIR = Path(os.getenv("LICENSE_KEY_DIR", "/run/secrets/medorax-license"))
ISSUER_TOKEN = os.getenv("LICENSE_ISSUER_TOKEN", "")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////data/licensing.db")

engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

class Base(DeclarativeBase): pass

class License(Base):
    __tablename__ = "license_issuer_licenses"
    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(128), index=True)
    plan: Mapped[str] = mapped_column(String(64))
    expires_at: Mapped[int] = mapped_column(Integer)
    max_devices: Mapped[int] = mapped_column(Integer)
    modules_json: Mapped[str] = mapped_column(Text)
    payload_json: Mapped[str] = mapped_column(Text)
    signature: Mapped[str] = mapped_column(Text)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[Any] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Any] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Activation(Base):
    __tablename__ = "license_issuer_activations"
    __table_args__ = (UniqueConstraint("license_id", "device_id", name="uq_issuer_license_device"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    license_id: Mapped[str] = mapped_column(String(128), index=True)
    device_id: Mapped[str] = mapped_column(String(255), index=True)
    device_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    activated_at: Mapped[int] = mapped_column(Integer)
    last_seen: Mapped[int] = mapped_column(Integer)

Base.metadata.create_all(engine)


def private_key() -> Ed25519PrivateKey:
    path = KEY_DIR / "private.pem"
    if not path.exists():
        raise HTTPException(503, "Issuer private key is not configured")
    return serialization.load_pem_private_key(path.read_bytes(), password=None)


def canonical(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()


def require_issuer(x_issuer_token: str | None) -> None:
    if not ISSUER_TOKEN or not secrets.compare_digest(x_issuer_token or "", ISSUER_TOKEN):
        raise HTTPException(401, "Unauthorized")


class LicenseRequest(BaseModel):
    tenant_id: str = Field(min_length=1, max_length=128)
    plan: str = Field(default="standard", min_length=1, max_length=64)
    expires_at: int
    max_devices: int = Field(default=1, ge=1, le=100)
    modules: list[str] = Field(default_factory=list)

class ActivationRequest(BaseModel):
    license: dict[str, Any]
    signature: str = Field(min_length=16)
    device_id: str = Field(min_length=8, max_length=255)
    device_name: str | None = Field(default=None, max_length=255)

class DeactivationRequest(BaseModel):
    license_id: str
    device_id: str

class ValidateRequest(BaseModel):
    license_id: str
    device_id: str

@APP.get("/health/live")
def live(): return {"status": "alive"}

@APP.get("/health/ready")
def ready():
    try:
        with engine.connect() as conn: conn.exec_driver_sql("SELECT 1")
        private_key()
        return {"status": "ready"}
    except Exception as exc:
        raise HTTPException(503, "Issuer not ready") from exc

@APP.post("/v1/licenses", status_code=201)
def issue(req: LicenseRequest, x_issuer_token: str | None = Header(default=None)):
    require_issuer(x_issuer_token)
    if req.expires_at <= int(time.time()): raise HTTPException(422, "expires_at must be in the future")
    payload = {"license_id": secrets.token_urlsafe(18), "product": "MEDORAX-ERP", **req.model_dump(), "issued_at": int(time.time()), "status": "active"}
    signature = base64.urlsafe_b64encode(private_key().sign(canonical(payload))).decode().rstrip("=")
    with SessionLocal() as db:
        db.add(License(id=payload["license_id"], tenant_id=req.tenant_id, plan=req.plan, expires_at=req.expires_at, max_devices=req.max_devices, modules_json=json.dumps(req.modules), payload_json=json.dumps(payload, separators=(",", ":"), sort_keys=True), signature=signature))
        db.commit()
    return {"license": payload, "signature": signature}

@APP.get("/v1/licenses/{license_id}")
def get_license(license_id: str, x_issuer_token: str | None = Header(default=None)):
    require_issuer(x_issuer_token)
    with SessionLocal() as db:
        row = db.get(License, license_id)
        if not row: raise HTTPException(404, "License not found")
        return {"license": json.loads(row.payload_json), "signature": row.signature, "revoked": row.revoked}

@APP.post("/v1/licenses/{license_id}/revoke")
def revoke(license_id: str, x_issuer_token: str | None = Header(default=None)):
    require_issuer(x_issuer_token)
    with SessionLocal() as db:
        row = db.get(License, license_id)
        if not row: raise HTTPException(404, "License not found")
        row.revoked = True
        payload = json.loads(row.payload_json); payload["status"] = "revoked"
        row.payload_json = json.dumps(payload, separators=(",", ":"), sort_keys=True)
        db.commit()
    return {"status": "revoked", "license_id": license_id}

@APP.post("/v1/licenses/{license_id}/renew")
def renew(license_id: str, expires_at: int, x_issuer_token: str | None = Header(default=None)):
    require_issuer(x_issuer_token)
    if expires_at <= int(time.time()): raise HTTPException(422, "expires_at must be in the future")
    with SessionLocal() as db:
        row = db.get(License, license_id)
        if not row: raise HTTPException(404, "License not found")
        payload = json.loads(row.payload_json); payload["expires_at"] = expires_at; payload["status"] = "active"
        row.expires_at = expires_at; row.revoked = False; row.payload_json = json.dumps(payload, separators=(",", ":"), sort_keys=True)
        row.signature = base64.urlsafe_b64encode(private_key().sign(canonical(payload))).decode().rstrip("=")
        db.commit()
        return {"license": payload, "signature": row.signature, "revoked": False}

@APP.post("/v1/activations")
def activate(req: ActivationRequest):
    with SessionLocal() as db:
        row = db.get(License, str(req.license.get("license_id")))
        if not row: raise HTTPException(404, "License not found")
        if row.revoked: raise HTTPException(403, "License is revoked")
        if row.signature != req.signature or row.payload_json != json.dumps(req.license, separators=(",", ":"), sort_keys=True): raise HTTPException(400, "License payload/signature mismatch")
        if row.expires_at <= int(time.time()): raise HTTPException(403, "License has expired")
        existing = db.query(Activation).filter(Activation.license_id == row.id, Activation.device_id == req.device_id).first()
        if not existing:
            active_count = db.query(Activation).filter(Activation.license_id == row.id, Activation.active.is_(True)).count()
            if active_count >= row.max_devices: raise HTTPException(409, "License device limit reached")
            existing = Activation(license_id=row.id, device_id=req.device_id, device_name=req.device_name, active=True, activated_at=int(time.time()), last_seen=int(time.time()))
            db.add(existing)
        else:
            existing.active = True; existing.device_name = req.device_name; existing.last_seen = int(time.time())
        db.commit()
    return {"status": "active", "license_id": row.id, "device_id": req.device_id}

@APP.post("/v1/activations/deactivate")
def deactivate(req: DeactivationRequest):
    with SessionLocal() as db:
        row = db.query(Activation).filter(Activation.license_id == req.license_id, Activation.device_id == req.device_id).first()
        if not row: raise HTTPException(404, "Activation not found")
        row.active = False; row.last_seen = int(time.time()); db.commit()
    return {"status": "deactivated"}

@APP.post("/v1/validate")
def validate(req: ValidateRequest):
    with SessionLocal() as db:
        row = db.get(License, req.license_id)
        if not row: return {"status": "invalid"}
        if row.revoked: return {"status": "revoked"}
        if row.expires_at <= int(time.time()): return {"status": "expired"}
        activation = db.query(Activation).filter(Activation.license_id == req.license_id, Activation.device_id == req.device_id, Activation.active.is_(True)).first()
        if not activation: return {"status": "inactive"}
        activation.last_seen = int(time.time()); db.commit()
        return {"status": "active", "license": json.loads(row.payload_json)}
