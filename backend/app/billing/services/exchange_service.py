from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException, ValidationException
from app.billing.models import ExchangeBill, Invoice, InvoiceItem
from app.billing.repository import BillingRepository
from app.billing.schemas import ExchangeBillCreate
from app.medicine.models import Medicine, MedicineBatch
from app.inventory.service import InventoryService

class ExchangeService:

    @staticmethod
    def exchange_medicine(
        db: Session,
        pharmacy_id: str,
        user_id: str,
        data: ExchangeBillCreate,
    ) -> ExchangeBill:
        # 1. Find Invoice
        invoice = BillingRepository.get_invoice_by_number(db, pharmacy_id, data.invoice_number)
        if not invoice:
            raise NotFoundException(f"Invoice '{data.invoice_number}'")

        # 2. Check Old Item in Invoice
        old_item = db.query(InvoiceItem).filter(
            InvoiceItem.invoice_id == invoice.id,
            InvoiceItem.medicine_id == data.old_medicine_id
        ).first()
        if not old_item:
            raise NotFoundException("Old medicine in invoice")

        if data.old_quantity > old_item.quantity:
            raise ValidationException(f"Return quantity ({data.old_quantity}) exceeds purchased quantity ({old_item.quantity})")

        # 3. Check New Medicine and Batch
        new_medicine = db.query(Medicine).filter(
            Medicine.id == data.new_medicine_id,
            Medicine.pharmacy_id == pharmacy_id
        ).first()
        if not new_medicine:
            raise NotFoundException("New medicine")

        if data.new_batch_number:
            new_batch = db.query(MedicineBatch).filter(
                MedicineBatch.medicine_id == new_medicine.id,
                MedicineBatch.batch_number == data.new_batch_number,
                MedicineBatch.status == "ACTIVE"
            ).first()
        else:
            new_batch = (
                db.query(MedicineBatch)
                .filter(
                    MedicineBatch.medicine_id == new_medicine.id,
                    MedicineBatch.quantity_available >= data.new_quantity,
                    MedicineBatch.status == "ACTIVE"
                )
                .order_by(MedicineBatch.expiry_date.asc())
                .first()
            )

        if not new_batch:
            raise ValidationException(f"No available active batch with sufficient stock for '{new_medicine.name}'")

        if new_batch.quantity_available < data.new_quantity:
            raise ValidationException(f"Insufficient stock for new medicine. Available: {new_batch.quantity_available}")

        # 4. Stock adjustments
        # Increase Old Medicine Stock
        old_batch = db.query(MedicineBatch).filter(
            MedicineBatch.medicine_id == old_item.medicine_id,
            MedicineBatch.batch_number == old_item.batch_number
        ).first()
        if old_batch:
            old_batch.quantity_available += data.old_quantity

        # Decrease New Medicine Stock
        new_batch.quantity_available -= data.new_quantity

        # 5. Price difference calculation
        old_unit_rate = Decimal(str(old_item.rate))
        old_total = (old_unit_rate * Decimal(data.old_quantity)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        new_unit_rate = Decimal(str(new_batch.selling_price))
        new_total = (new_unit_rate * Decimal(data.new_quantity)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        price_diff = (new_total - old_total).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # 6. Inventory Ledger Logs
        InventoryService.record_return(
            db=db,
            pharmacy_id=pharmacy_id,
            medicine_id=old_item.medicine_id,
            batch_number=old_item.batch_number,
            quantity=data.old_quantity,
            invoice_number=invoice.invoice_number,
            branch_id=data.branch_id or invoice.branch_id,
            user_id=user_id,
        )

        InventoryService.record_sale(
            db=db,
            pharmacy_id=pharmacy_id,
            medicine_id=new_medicine.id,
            batch_number=new_batch.batch_number,
            quantity=data.new_quantity,
            invoice_number=invoice.invoice_number,
            branch_id=data.branch_id or invoice.branch_id,
            user_id=user_id,
        )

        # 7. Create Exchange Bill
        exchange_bill = ExchangeBill(
            pharmacy_id=pharmacy_id,
            branch_id=data.branch_id or invoice.branch_id,
            invoice_id=invoice.id,
            invoice_number=invoice.invoice_number,
            old_medicine_id=old_item.medicine_id,
            old_medicine_name=old_item.medicine_name,
            old_batch_number=old_item.batch_number,
            old_quantity=data.old_quantity,
            new_medicine_id=new_medicine.id,
            new_medicine_name=new_medicine.name,
            new_batch_number=new_batch.batch_number,
            new_quantity=data.new_quantity,
            price_difference=price_diff,
            created_by_user_id=user_id,
        )

        return BillingRepository.create_exchange_bill(db, exchange_bill)
