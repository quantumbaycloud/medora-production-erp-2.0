from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime

class SettingBase(BaseModel):
    company_name: Optional[str] = None
    default_gst_percentage: Decimal = Field(default=Decimal("18.00"), max_digits=10, decimal_places=2, ge=0)
    invoice_template: str = "Standard Clean Layout"
    printer_settings: str = "Thermal 80mm"
    barcode_settings: str = "Code128"
    backup_settings: str = "Daily Auto-Backup"
    session_timeout_minutes: int = Field(default=30, ge=5, le=1440)
    maintenance_mode: bool = False
    audit_log_retention_days: int = Field(default=365, ge=30, le=3650)

class SettingUpdate(BaseModel):
    company_name: Optional[str] = None
    default_gst_percentage: Optional[Decimal] = None
    invoice_template: Optional[str] = None
    printer_settings: Optional[str] = None
    barcode_settings: Optional[str] = None
    backup_settings: Optional[str] = None
    session_timeout_minutes: Optional[int] = Field(None, ge=5, le=1440)
    maintenance_mode: Optional[bool] = None
    audit_log_retention_days: Optional[int] = Field(None, ge=30, le=3650)

class SettingResponse(SettingBase):
    id: str
    pharmacy_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
