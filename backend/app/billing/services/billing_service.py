import json
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException, ValidationException
from app.billing.models import Invoice, InvoiceItem, HoldBill
from app.billing.repository import BillingRepository
from app.billing.schemas import GenerateInvoiceRequest, QuickBillingRequest, BillingItemRequest
from app.medicine.models import Medicine, MedicineBatch
from app.customer.models import Customer
from app.inventory.service import InventoryService
from app.audit.service import AuditService

class BillingService:

    @staticmethod
    def generate_invoice(
        db: Session,
        pharmacy_id: str,
        user_id: str,
        data: GenerateInvoiceRequest,
    ) -> Invoice:
        # Validate Customer if provided
        customer = None
        if data.customer_id:
            customer = db.query(Customer).filter(
                Customer.id == data.customer_id,
                Customer.pharmacy_id == pharmacy_id
            ).first()
            if not customer:
                raise NotFoundException("Customer")

        customer_name = (
            data.customer_name
            or (customer.customer_name if customer else "Walk-in Customer")
        )

        grand_total = Decimal("0.00")
        total_discount = Decimal("0.00")
        total_tax = Decimal("0.00")
        invoice_items = []
        batches_to_update = []

        for req_item in data.items:
            # 1. Fetch medicine
            medicine = db.query(Medicine).filter(
                Medicine.id == req_item.medicine_id,
                Medicine.pharmacy_id == pharmacy_id
            ).first()
            if not medicine:
                raise NotFoundException(f"Medicine with ID {req_item.medicine_id}")

            # 2. Select Batch with row-level lock (FOR UPDATE)
            if req_item.batch_number:
                batch = db.query(MedicineBatch).filter(
                    MedicineBatch.medicine_id == medicine.id,
                    MedicineBatch.batch_number == req_item.batch_number,
                    MedicineBatch.status == "ACTIVE"
                ).with_for_update().first()
            else:
                # FIFO / Earliest Expiry Active Batch with stock
                batch = (
                    db.query(MedicineBatch)
                    .filter(
                        MedicineBatch.medicine_id == medicine.id,
                        MedicineBatch.quantity_available >= req_item.quantity,
                        MedicineBatch.status == "ACTIVE"
                    )
                    .order_by(MedicineBatch.expiry_date.asc())
                    .with_for_update()
                    .first()
                )

            if not batch:
                raise ValidationException(f"No available active batch with sufficient stock for '{medicine.name}'")

            if batch.expiry_date < date.today():
                raise ValidationException(f"Selected batch '{batch.batch_number}' for '{medicine.name}' is expired")

            if batch.quantity_available < req_item.quantity:
                raise ValidationException(f"Insufficient stock for '{medicine.name}' batch '{batch.batch_number}'. Requested: {req_item.quantity}, Available: {batch.quantity_available}")

            # 3. Calculations
            rate = Decimal(str(batch.selling_price))
            subtotal = rate * Decimal(req_item.quantity)

            # Discount calculation
            discount_amount = Decimal("0.00")
            if req_item.discount_type:
                d_type = req_item.discount_type.lower()
                d_val = Decimal(str(req_item.discount_value))
                if d_type == "percentage":
                    if d_val < 0 or d_val > 100:
                        raise ValidationException("Percentage discount must be between 0 and 100")
                    discount_amount = (subtotal * d_val) / Decimal("100")
                elif d_type == "flat":
                    if d_val > subtotal:
                        raise ValidationException("Flat discount cannot exceed item subtotal")
                    discount_amount = d_val
                else:
                    raise ValidationException(f"Invalid discount type: '{req_item.discount_type}'")

            net_amount = subtotal - discount_amount

            # GST calculation
            gst_pct = Decimal(str(medicine.gst_percentage or Decimal("0.00")))
            gst_amount = (net_amount * gst_pct) / Decimal("100")
            item_total = net_amount + gst_amount

            # Accumulate totals
            grand_total += item_total
            total_discount += discount_amount
            total_tax += gst_amount

            item = InvoiceItem(
                medicine_id=medicine.id,
                batch_id=batch.id,
                medicine_name=medicine.name,
                batch_number=batch.batch_number,
                quantity=req_item.quantity,
                rate=rate,
                discount=discount_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                gst_percentage=gst_pct,
                gst_amount=gst_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                total_amount=item_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            )
            invoice_items.append((item, batch, req_item.quantity))

        grand_total = grand_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total_discount = total_discount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total_tax = total_tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # 4. Payment validation
        p_method = data.payment_method.title()
        valid_methods = ["Cash", "Card", "Upi", "Wallet", "Split Payment", "Credit"]
        if p_method not in valid_methods:
            raise ValidationException(f"Invalid payment method: '{data.payment_method}'")

        payment_status = "Pending" if data.is_credit else "Paid"

        if p_method == "Split Payment":
            paid_sum = data.cash_amount + data.card_amount + data.upi_amount + data.wallet_amount
            if paid_sum.quantize(Decimal("0.01")) != grand_total:
                raise ValidationException(f"Split payment total ({paid_sum}) must equal grand total ({grand_total})")

        # 5. Create Invoice
        inv_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S%f')[:17]}"
        invoice = Invoice(
            pharmacy_id=pharmacy_id,
            branch_id=data.branch_id,
            customer_id=customer.id if customer else None,
            invoice_number=inv_number,
            customer_name=customer_name,
            total_amount=grand_total,
            discount_amount=total_discount,
            tax_amount=total_tax,
            payment_method=p_method,
            payment_status=payment_status,
            cash_amount=data.cash_amount,
            card_amount=data.card_amount,
            upi_amount=data.upi_amount,
            wallet_amount=data.wallet_amount,
            created_by_user_id=user_id,
            items=[it[0] for it in invoice_items],
        )

        db.add(invoice)

        # 6. Deduct stock & create Inventory Ledger logs
        for item, batch, qty in invoice_items:
            batch.quantity_available -= qty
            InventoryService.record_sale(
                db=db,
                pharmacy_id=pharmacy_id,
                medicine_id=item.medicine_id,
                batch_number=batch.batch_number,
                quantity=qty,
                invoice_number=inv_number,
                branch_id=data.branch_id,
                user_id=user_id,
            )

        # 7. Customer credit balance update
        if data.is_credit and customer:
            customer.outstanding_amount += grand_total

        AuditService.log(
            db=db,
            pharmacy_id=pharmacy_id,
            action_type="INVOICE_CREATED",
            category="Sales",
            user_id=user_id,
            entity_type="Invoice",
            entity_id=invoice.id,
            details={"invoice_number": inv_number, "total_amount": float(grand_total)}
        )

        db.flush()
        return invoice

    @staticmethod
    def quick_billing(
        db: Session,
        pharmacy_id: str,
        user_id: str,
        data: QuickBillingRequest,
    ) -> Invoice:
        req = GenerateInvoiceRequest(
            branch_id=data.branch_id,
            items=[
                BillingItemRequest(
                    medicine_id=data.medicine_id,
                    batch_number=data.batch_number,
                    quantity=data.quantity,
                )
            ],
            payment_method=data.payment_method,
        )
        return BillingService.generate_invoice(db, pharmacy_id, user_id, req)
