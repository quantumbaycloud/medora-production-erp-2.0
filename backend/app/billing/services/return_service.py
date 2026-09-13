from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException, ValidationException
from app.billing.models import ReturnBill, Invoice, InvoiceItem
from app.billing.repository import BillingRepository
from app.billing.schemas import ReturnBillCreate
from app.medicine.models import MedicineBatch
from app.inventory.service import InventoryService
from app.audit.service import AuditService

class ReturnService:

    @staticmethod
    def return_medicine(
        db: Session,
        pharmacy_id: str,
        user_id: str,
        data: ReturnBillCreate,
    ) -> ReturnBill:
        # Find Invoice
        invoice = BillingRepository.get_invoice_by_number(db, pharmacy_id, data.invoice_number)
        if not invoice:
            raise NotFoundException(f"Invoice '{data.invoice_number}'")

        # Find Item in Invoice
        item = db.query(InvoiceItem).filter(
            InvoiceItem.invoice_id == invoice.id,
            InvoiceItem.medicine_id == data.medicine_id
        ).first()
        if not item:
            raise NotFoundException("Medicine in this invoice")

        if data.quantity > item.quantity:
            raise ValidationException(f"Return quantity ({data.quantity}) exceeds purchased quantity ({item.quantity})")

        # Calculate unit refund
        unit_price = (item.total_amount / Decimal(item.quantity)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        refund_amount = (unit_price * Decimal(data.quantity)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # Restore Stock to batch
        batch = db.query(MedicineBatch).filter(
            MedicineBatch.medicine_id == item.medicine_id,
            MedicineBatch.batch_number == item.batch_number
        ).with_for_update().first()

        if batch:
            batch.quantity_available += data.quantity

        invoice.status = "Refunded"

        AuditService.log(
            db=db,
            pharmacy_id=pharmacy_id,
            action_type="RETURN_PROCESSED",
            category="Sales",
            user_id=user_id,
            entity_type="Invoice",
            entity_id=invoice.id,
            details={"invoice_number": invoice.invoice_number, "refund_amount": float(refund_amount)}
        )

        db.flush()

        # Record Return in Inventory Ledger
        InventoryService.record_return(
            db=db,
            pharmacy_id=pharmacy_id,
            medicine_id=item.medicine_id,
            batch_number=item.batch_number,
            quantity=data.quantity,
            invoice_number=invoice.invoice_number,
            branch_id=data.branch_id or invoice.branch_id,
            user_id=user_id,
        )

        # Create Return Bill Record
        return_bill = ReturnBill(
            pharmacy_id=pharmacy_id,
            branch_id=data.branch_id or invoice.branch_id,
            invoice_id=invoice.id,
            invoice_number=invoice.invoice_number,
            medicine_id=item.medicine_id,
            medicine_name=item.medicine_name,
            batch_number=item.batch_number,
            quantity=data.quantity,
            refund_amount=refund_amount,
            reason=data.reason,
            created_by_user_id=user_id,
        )

        return BillingRepository.create_return_bill(db, return_bill)
