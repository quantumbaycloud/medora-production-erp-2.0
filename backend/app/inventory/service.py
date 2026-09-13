from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, ValidationException
from app.inventory.models import InventoryLedger
from app.inventory.repository import InventoryRepository
from app.inventory.schemas import StockAdjustmentCreate
from app.medicine.models import MedicineBatch, Medicine

class InventoryService:

    @staticmethod
    def get_ledger(
        db: Session,
        pharmacy_id: str,
        medicine_id: str = None,
        batch_number: str = None,
        transaction_type: str = None,
        branch_id: str = None,
    ) -> list[InventoryLedger]:
        return InventoryRepository.get_ledger(
            db,
            pharmacy_id=pharmacy_id,
            medicine_id=medicine_id,
            batch_number=batch_number,
            transaction_type=transaction_type,
            branch_id=branch_id,
        )

    @staticmethod
    def record_sale(
        db: Session,
        pharmacy_id: str,
        medicine_id: str,
        batch_number: str,
        quantity: int,
        invoice_number: str,
        branch_id: str = None,
        user_id: str = None,
    ) -> InventoryLedger:
        return InventoryRepository.create_log(
            db=db,
            pharmacy_id=pharmacy_id,
            medicine_id=medicine_id,
            batch_number=batch_number,
            transaction_type="SALE",
            quantity=-abs(quantity),
            reference_id=invoice_number,
            branch_id=branch_id,
            user_id=user_id,
        )

    @staticmethod
    def record_return(
        db: Session,
        pharmacy_id: str,
        medicine_id: str,
        batch_number: str,
        quantity: int,
        invoice_number: str,
        branch_id: str = None,
        user_id: str = None,
    ) -> InventoryLedger:
        return InventoryRepository.create_log(
            db=db,
            pharmacy_id=pharmacy_id,
            medicine_id=medicine_id,
            batch_number=batch_number,
            transaction_type="RETURN",
            quantity=abs(quantity),
            reference_id=invoice_number,
            branch_id=branch_id,
            user_id=user_id,
        )

    @staticmethod
    def adjust_stock(
        db: Session,
        pharmacy_id: str,
        user_id: str,
        data: StockAdjustmentCreate,
        branch_id: str = None,
    ) -> InventoryLedger:
        # Validate medicine and batch
        medicine = db.query(Medicine).filter(Medicine.id == data.medicine_id, Medicine.pharmacy_id == pharmacy_id).first()
        if not medicine:
            raise NotFoundException("Medicine")

        batch = db.query(MedicineBatch).filter(
            MedicineBatch.medicine_id == data.medicine_id,
            MedicineBatch.batch_number == data.batch_number
        ).first()
        if not batch:
            raise NotFoundException("MedicineBatch")

        new_qty = batch.quantity_available + data.quantity_delta
        if new_qty < 0:
            raise ValidationException("Adjustment would cause batch quantity to fall below 0")

        batch.quantity_available = new_qty

        ledger_entry = InventoryRepository.create_log(
            db=db,
            pharmacy_id=pharmacy_id,
            medicine_id=data.medicine_id,
            batch_number=data.batch_number,
            transaction_type="ADJUSTMENT",
            quantity=data.quantity_delta,
            branch_id=branch_id,
            user_id=user_id,
            notes=data.reason,
        )
        db.flush()
        return ledger_entry
