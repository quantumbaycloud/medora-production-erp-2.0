from sqlalchemy.orm import Session
from app.inventory.models import InventoryLedger

class InventoryRepository:

    @staticmethod
    def create_log(
        db: Session,
        pharmacy_id: str,
        medicine_id: str,
        batch_number: str,
        transaction_type: str,
        quantity: int,
        reference_id: str = None,
        branch_id: str = None,
        user_id: str = None,
        notes: str = None,
    ) -> InventoryLedger:
        log = InventoryLedger(
            pharmacy_id=pharmacy_id,
            branch_id=branch_id,
            medicine_id=medicine_id,
            batch_number=batch_number,
            transaction_type=transaction_type,
            quantity=quantity,
            reference_id=reference_id,
            created_by_user_id=user_id,
            notes=notes,
        )
        db.add(log)
        db.flush()
        return log

    @staticmethod
    def get_ledger(
        db: Session,
        pharmacy_id: str,
        medicine_id: str = None,
        batch_number: str = None,
        transaction_type: str = None,
        branch_id: str = None,
    ) -> list[InventoryLedger]:
        q = db.query(InventoryLedger).filter(InventoryLedger.pharmacy_id == pharmacy_id)
        if medicine_id:
            q = q.filter(InventoryLedger.medicine_id == medicine_id)
        if batch_number:
            q = q.filter(InventoryLedger.batch_number == batch_number)
        if transaction_type:
            q = q.filter(InventoryLedger.transaction_type == transaction_type)
        if branch_id:
            q = q.filter(InventoryLedger.branch_id == branch_id)

        return q.order_by(InventoryLedger.created_at.desc()).all()
