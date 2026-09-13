from decimal import Decimal
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, ValidationException
from app.purchase.models import PurchaseInvoice, PurchaseItem
from app.purchase.repository import PurchaseRepository
from app.purchase.schemas import PurchaseInvoiceCreate, PurchaseInvoiceUpdate
from app.supplier.service import SupplierService
from app.medicine.models import Medicine, MedicineBatch
from app.medicine.repository import MedicineRepository
from app.audit.service import AuditService

class PurchaseService:

    @staticmethod
    def create_purchase(
        db: Session,
        pharmacy_id: str,
        user_id: str,
        data: PurchaseInvoiceCreate
    ) -> PurchaseInvoice:
        # Validate supplier exists for this pharmacy
        SupplierService.get_supplier(db, pharmacy_id, data.supplier_id)

        # Calculate totals for items
        purchase_items = []
        grand_total = Decimal("0.00")

        for item_data in data.items:
            # Validate medicine exists
            medicine = MedicineRepository.get_medicine(db, pharmacy_id, item_data.medicine_id)
            if not medicine:
                raise NotFoundException(f"Medicine with ID {item_data.medicine_id}")

            # Item subtotal before tax/discount
            base_amount = Decimal(str(item_data.purchase_price)) * Decimal(item_data.quantity)
            discount_amount = base_amount * (Decimal(str(item_data.discount_percentage)) / Decimal("100"))
            amount_after_discount = base_amount - discount_amount
            tax_amount = amount_after_discount * (Decimal(str(item_data.tax_percentage)) / Decimal("100"))
            item_total = amount_after_discount + tax_amount

            grand_total += item_total

            item = PurchaseItem(
                medicine_id=item_data.medicine_id,
                batch_number=item_data.batch_number,
                expiry_date=item_data.expiry_date,
                quantity=item_data.quantity,
                free_quantity=item_data.free_quantity,
                purchase_price=item_data.purchase_price,
                mrp=item_data.mrp,
                selling_price=item_data.selling_price,
                tax_percentage=item_data.tax_percentage,
                discount_percentage=item_data.discount_percentage,
                total_amount=item_total,
            )
            purchase_items.append(item)

        is_paid = (data.paid_amount >= grand_total)

        purchase = PurchaseInvoice(
            pharmacy_id=pharmacy_id,
            branch_id=data.branch_id,
            supplier_id=data.supplier_id,
            invoice_number=data.invoice_number,
            invoice_date=data.invoice_date,
            total_amount=grand_total,
            paid_amount=data.paid_amount,
            is_paid=is_paid,
            status="DRAFT",
            notes=data.notes,
            created_by_user_id=user_id,
            items=purchase_items,
        )

        created_purchase = PurchaseRepository.create_purchase(db, purchase)
        return created_purchase

    @staticmethod
    def get_purchase(db: Session, pharmacy_id: str, purchase_id: str) -> PurchaseInvoice:
        purchase = PurchaseRepository.get_purchase(db, pharmacy_id, purchase_id)
        if not purchase:
            raise NotFoundException("PurchaseInvoice")
        return purchase

    @staticmethod
    def list_purchases(
        db: Session,
        pharmacy_id: str,
        supplier_id: str = None,
        branch_id: str = None,
        status: str = None
    ) -> list[PurchaseInvoice]:
        return PurchaseRepository.list_purchases(db, pharmacy_id, supplier_id, branch_id, status)

    @staticmethod
    def update_purchase(
        db: Session,
        pharmacy_id: str,
        purchase_id: str,
        data: PurchaseInvoiceUpdate
    ) -> PurchaseInvoice:
        purchase = PurchaseService.get_purchase(db, pharmacy_id, purchase_id)
        if purchase.status != "DRAFT":
            raise ValidationException(f"Cannot update purchase in '{purchase.status}' status")
        return PurchaseRepository.update_purchase(db, purchase, data)

    @staticmethod
    def approve_purchase(
        db: Session,
        pharmacy_id: str,
        user_id: str,
        purchase_id: str
    ) -> PurchaseInvoice:
        purchase = PurchaseService.get_purchase(db, pharmacy_id, purchase_id)
        if purchase.status != "DRAFT":
            raise ValidationException(f"Purchase is already '{purchase.status}'")

        # Inward goods to MedicineBatch inventory
        for item in purchase.items:
            # Check if batch exists
            batch = db.query(MedicineBatch).filter(
                MedicineBatch.medicine_id == item.medicine_id,
                MedicineBatch.batch_number == item.batch_number
            ).with_for_update().first()

            total_received_qty = item.quantity + item.free_quantity

            if batch:
                batch.quantity_available += total_received_qty
                batch.purchase_price = item.purchase_price
                batch.selling_price = item.selling_price
                batch.mrp = item.mrp
                batch.expiry_date = item.expiry_date
                batch.status = "ACTIVE"
            else:
                batch = MedicineBatch(
                    medicine_id=item.medicine_id,
                    batch_number=item.batch_number,
                    expiry_date=item.expiry_date,
                    purchase_price=item.purchase_price,
                    selling_price=item.selling_price,
                    mrp=item.mrp,
                    quantity_available=total_received_qty,
                    status="ACTIVE",
                )
                db.add(batch)

        purchase.status = "APPROVED"
        purchase.approved_by_user_id = user_id

        AuditService.log(
            db=db,
            pharmacy_id=pharmacy_id,
            action_type="PURCHASE_APPROVED",
            category="Purchases",
            user_id=user_id,
            entity_type="PurchaseInvoice",
            entity_id=purchase.id,
            details={"invoice_number": purchase.invoice_number, "total_amount": float(purchase.total_amount)}
        )

        db.flush()
        return purchase
