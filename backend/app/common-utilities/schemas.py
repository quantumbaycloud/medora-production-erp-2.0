"""Pydantic (v2) schemas used for API request/response validation."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ErrorLogCreate(BaseModel):
    level: str = "ERROR"
    source: str
    message: str
    stack_trace: Optional[str] = None
    request_path: Optional[str] = None
    user_id: Optional[str] = None


class ErrorLogOut(ErrorLogCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    timestamp: datetime


class ActivityLogCreate(BaseModel):
    user_id: Optional[str] = None
    action: str
    resource: Optional[str] = None
    ip_address: Optional[str] = None
    status: str = "SUCCESS"
    details: Optional[str] = None


class ActivityLogOut(ActivityLogCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    timestamp: datetime


class SystemLogCreate(BaseModel):
    level: str = "INFO"
    component: str
    message: str


class SystemLogOut(SystemLogCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    timestamp: datetime


class HealthCheckOut(BaseModel):
    status: str                 # "healthy" | "degraded" | "unhealthy"
    timestamp: datetime
    uptime_seconds: float
    checks: dict                # per-component breakdown (db, disk, memory, cpu)
