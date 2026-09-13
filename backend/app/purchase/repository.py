from sqlalchemy.orm import Session, joinedload
from app.purchase.models import PurchaseInvoice, PurchaseItem
from app.purchase.schemas import PurchaseInvoiceUpdate

class PurchaseRepository:

    @staticmethod
    def create_purchase(db: Session, purchase: PurchaseInvoice) -> PurchaseInvoice:
        db.add(purchase)
        db.flush()
        return purchase

    @staticmethod
    def get_purchase(db: Session, pharmacy_id: str, purchase_id: str) -> PurchaseInvoice | None:
        return db.query(PurchaseInvoice).options(
            joinedload(PurchaseInvoice.items).joinedload(PurchaseItem.medicine),
            joinedload(PurchaseInvoice.supplier),
            joinedload(PurchaseInvoice.branch),
        ).filter(
            PurchaseInvoice.id == purchase_id,
            PurchaseInvoice.pharmacy_id == pharmacy_id
        ).first()

    @staticmethod
    def list_purchases(
        db: Session,
        pharmacy_id: str,
        supplier_id: str = None,
        branch_id: str = None,
        status: str = None
    ) -> list[PurchaseInvoice]:
        q = db.query(PurchaseInvoice).options(
            joinedload(PurchaseInvoice.supplier),
            joinedload(PurchaseInvoice.branch),
        ).filter(PurchaseInvoice.pharmacy_id == pharmacy_id)

        if supplier_id:
            q = q.filter(PurchaseInvoice.supplier_id == supplier_id)
        if branch_id:
            q = q.filter(PurchaseInvoice.branch_id == branch_id)
        if status:
            q = q.filter(PurchaseInvoice.status == status)

        return q.order_by(PurchaseInvoice.created_at.desc()).all()

    @staticmethod
    def update_purchase(db: Session, purchase: PurchaseInvoice, data: PurchaseInvoiceUpdate) -> PurchaseInvoice:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(purchase, key, value)
        if purchase.paid_amount >= purchase.total_amount:
            purchase.is_paid = True
        else:
            purchase.is_paid = False
        db.flush()
        return purchase
