import json
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.billing.models import HoldBill
from app.billing.repository import BillingRepository
from app.billing.schemas import HoldBillCreate, HoldBillResponse
from app.medicine.models import Medicine, MedicineBatch
from app.customer.models import Customer

class HoldService:

    @staticmethod
    def hold_bill(
        db: Session,
        pharmacy_id: str,
        user_id: str,
        data: HoldBillCreate,
    ) -> HoldBillResponse:
        customer_name = data.customer_name
        if data.customer_id:
            c = db.query(Customer).filter(Customer.id == data.customer_id, Customer.pharmacy_id == pharmacy_id).first()
            if c:
                customer_name = c.customer_name

        total_amount = Decimal("0.00")
        items_payload = []

        for req_item in data.items:
            med = db.query(Medicine).filter(Medicine.id == req_item.medicine_id, Medicine.pharmacy_id == pharmacy_id).first()
            if med:
                batch = None
                if req_item.batch_number:
                    batch = db.query(MedicineBatch).filter(
                        MedicineBatch.medicine_id == med.id,
                        MedicineBatch.batch_number == req_item.batch_number
                    ).first()
                else:
                    batch = db.query(MedicineBatch).filter(MedicineBatch.medicine_id == med.id).first()

                rate = batch.selling_price if batch else Decimal("0.00")
                item_total = Decimal(str(rate)) * Decimal(req_item.quantity)
                total_amount += item_total

                items_payload.append({
                    "medicine_id": med.id,
                    "medicine_name": med.name,
                    "batch_number": req_item.batch_number or (batch.batch_number if batch else ""),
                    "quantity": req_item.quantity,
                    "rate": float(rate),
                    "total": float(item_total),
                    "discount_type": req_item.discount_type,
                    "discount_value": float(req_item.discount_value),
                })

        hold_number = f"HOLD-{datetime.now().strftime('%Y%m%d%H%M%S%f')[:17]}"

        hold = HoldBill(
            pharmacy_id=pharmacy_id,
            branch_id=data.branch_id,
            customer_id=data.customer_id,
            hold_number=hold_number,
            customer_name=customer_name or "Walk-in Customer",
            items_json=json.dumps(items_payload),
            total_amount=total_amount,
            status="HOLD",
            created_by_user_id=user_id,
        )

        db.add(hold)
        db.flush()

        return HoldBillResponse(
            id=hold.id,
            hold_number=hold.hold_number,
            customer_name=hold.customer_name,
            total_amount=hold.total_amount,
            status=hold.status,
            created_at=hold.created_at,
            items=items_payload,
        )

    @staticmethod
    def resume_bill(db: Session, pharmacy_id: str, hold_number: str) -> HoldBillResponse:
        hold = BillingRepository.get_hold_bill(db, pharmacy_id, hold_number)
        if not hold:
            raise NotFoundException(f"Hold bill '{hold_number}'")

        items = []
        try:
            items = json.loads(hold.items_json)
        except Exception:
            pass

        return HoldBillResponse(
            id=hold.id,
            hold_number=hold.hold_number,
            customer_name=hold.customer_name,
            total_amount=hold.total_amount,
            status=hold.status,
            created_at=hold.created_at,
            items=items,
        )
