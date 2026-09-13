from fastapi import APIRouter, Depends, Query, Response, status
from fastapi.responses import StreamingResponse, PlainTextResponse
from sqlalchemy.orm import Session
from typing import Optional

from app.db.base import get_db
from app.licensing.deps import get_current_licensed_user
from app.user.models import User
from app.staff.service import get_current_pharmacy_id
from app.staff.permissions import Permissions
from app.billing.schemas import (
    GenerateInvoiceRequest,
    QuickBillingRequest,
    InvoiceResponse,
    HoldBillCreate,
    HoldBillResponse,
    ReturnBillCreate,
    ReturnBillResponse,
    ExchangeBillCreate,
    ExchangeBillResponse,
)
from app.billing.services.billing_service import BillingService
from app.billing.services.return_service import ReturnService
from app.billing.services.exchange_service import ExchangeService
from app.billing.services.hold_service import HoldService
from app.billing.services.print_service import PrintService
from app.billing.repository import BillingRepository
from app.core.exceptions import NotFoundException

router = APIRouter(tags=["Billing & Sales"])

# --- Invoicing & Checkout ---

@router.post("/billing/items", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
@router.post("/billing/invoice", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_invoice(
    data: GenerateInvoiceRequest,
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.BILLING_CREATE.code)
    return BillingService.generate_invoice(db, active_pharmacy_id, current_user.id, data)

@router.post("/billing/quick", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def quick_billing(
    data: QuickBillingRequest,
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.BILLING_CREATE.code)
    return BillingService.quick_billing(db, active_pharmacy_id, current_user.id, data)


# --- Hold Bills ---

@router.post("/billing/hold", response_model=HoldBillResponse, status_code=status.HTTP_201_CREATED)
def hold_bill(
    data: HoldBillCreate,
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.BILLING_CREATE.code)
    return HoldService.hold_bill(db, active_pharmacy_id, current_user.id, data)

@router.get("/billing/hold/{hold_number}", response_model=HoldBillResponse)
def resume_hold_bill(
    hold_number: str,
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.BILLING_CREATE.code)
    return HoldService.resume_bill(db, active_pharmacy_id, hold_number)


# --- Returns & Exchanges ---

@router.post("/billing/returns", response_model=ReturnBillResponse, status_code=status.HTTP_201_CREATED)
def return_medicine(
    data: ReturnBillCreate,
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    # Segregation of duties: refund / return requires BILLING_REFUND
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.BILLING_REFUND.code)
    return ReturnService.return_medicine(db, active_pharmacy_id, current_user.id, data)

@router.post("/billing/exchanges", response_model=ExchangeBillResponse, status_code=status.HTTP_201_CREATED)
def exchange_medicine(
    data: ExchangeBillCreate,
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.BILLING_CREATE.code)
    return ExchangeService.exchange_medicine(db, active_pharmacy_id, current_user.id, data)


# --- Invoices & Printing ---

@router.get("/invoices/{invoice_number}", response_model=InvoiceResponse)
def get_invoice(
    invoice_number: str,
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.BILLING_CREATE.code)
    invoice = BillingRepository.get_invoice_by_number(db, active_pharmacy_id, invoice_number)
    if not invoice:
        raise NotFoundException(f"Invoice '{invoice_number}'")
    return invoice

@router.get("/invoices/{invoice_number}/thermal")
def print_thermal_invoice(
    invoice_number: str,
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.BILLING_CREATE.code)
    invoice = BillingRepository.get_invoice_by_number(db, active_pharmacy_id, invoice_number)
    if not invoice:
        raise NotFoundException(f"Invoice '{invoice_number}'")
    text_receipt = PrintService.generate_thermal_receipt(invoice)
    return PlainTextResponse(text_receipt, media_type="text/plain")

@router.get("/invoices/{invoice_number}/a4")
def print_a4_invoice(
    invoice_number: str,
    pharmacy_id: Optional[str] = Query(None, description="Optional Pharmacy ID context"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user)
):
    active_pharmacy_id = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.BILLING_CREATE.code)
    invoice = BillingRepository.get_invoice_by_number(db, active_pharmacy_id, invoice_number)
    if not invoice:
        raise NotFoundException(f"Invoice '{invoice_number}'")
    pdf_buffer = PrintService.generate_a4_pdf(invoice)
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename={invoice_number}.pdf"}
    )
