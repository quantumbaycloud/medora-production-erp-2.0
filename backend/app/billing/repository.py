from sqlalchemy.orm import Session, joinedload
from app.billing.models import Invoice, InvoiceItem, HoldBill, ReturnBill, ExchangeBill

class BillingRepository:

    @staticmethod
    def create_invoice(db: Session, invoice: Invoice) -> Invoice:
        db.add(invoice)
        db.flush()
        return invoice

    @staticmethod
    def get_invoice_by_number(db: Session, pharmacy_id: str, invoice_number: str) -> Invoice | None:
        return db.query(Invoice).options(
            joinedload(Invoice.items).joinedload(InvoiceItem.medicine),
            joinedload(Invoice.customer)
        ).filter(
            Invoice.invoice_number == invoice_number,
            Invoice.pharmacy_id == pharmacy_id
        ).first()

    @staticmethod
    def create_hold_bill(db: Session, hold: HoldBill) -> HoldBill:
        db.add(hold)
        db.flush()
        return hold

    @staticmethod
    def get_hold_bill(db: Session, pharmacy_id: str, hold_number: str) -> HoldBill | None:
        return db.query(HoldBill).filter(
            HoldBill.hold_number == hold_number,
            HoldBill.pharmacy_id == pharmacy_id
        ).first()

    @staticmethod
    def create_return_bill(db: Session, return_bill: ReturnBill) -> ReturnBill:
        db.add(return_bill)
        db.flush()
        return return_bill

    @staticmethod
    def create_exchange_bill(db: Session, exchange_bill: ExchangeBill) -> ExchangeBill:
        db.add(exchange_bill)
        db.flush()
        return exchange_bill
