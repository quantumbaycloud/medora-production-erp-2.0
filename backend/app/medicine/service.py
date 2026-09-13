from datetime import date
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, ValidationException
from app.medicine.models import Medicine, MedicineBatch
from app.medicine.repository import MedicineRepository
from app.medicine.schemas import MedicineCreate, MedicineUpdate, MedicineBatchCreate, MedicineBatchUpdate

class MedicineService:

    @staticmethod
    def create_medicine(db: Session, pharmacy_id: str, data: MedicineCreate) -> Medicine:
        if data.barcode:
            existing = MedicineRepository.get_medicine_by_barcode(db, pharmacy_id, data.barcode)
            if existing:
                raise ValidationException(f"Medicine with barcode {data.barcode} already exists.")
        return MedicineRepository.create_medicine(db, pharmacy_id, data)

    @staticmethod
    def get_medicine(db: Session, pharmacy_id: str, medicine_id: str) -> Medicine:
        medicine = MedicineRepository.get_medicine(db, pharmacy_id, medicine_id)
        if not medicine:
            raise NotFoundException("Medicine")
        return medicine

    @staticmethod
    def search_medicines(db: Session, pharmacy_id: str, query: str = None) -> list[Medicine]:
        return MedicineRepository.search_medicines(db, pharmacy_id, query)

    @staticmethod
    def update_medicine(db: Session, pharmacy_id: str, medicine_id: str, data: MedicineUpdate) -> Medicine:
        medicine = MedicineService.get_medicine(db, pharmacy_id, medicine_id)
        if data.barcode and data.barcode != medicine.barcode:
            existing = MedicineRepository.get_medicine_by_barcode(db, pharmacy_id, data.barcode)
            if existing:
                raise ValidationException(f"Medicine with barcode {data.barcode} already exists.")
        return MedicineRepository.update_medicine(db, medicine, data)

    @staticmethod
    def add_batch(db: Session, pharmacy_id: str, medicine_id: str, data: MedicineBatchCreate) -> MedicineBatch:
        # Ensure medicine exists in this pharmacy
        MedicineService.get_medicine(db, pharmacy_id, medicine_id)
        return MedicineRepository.create_batch(db, medicine_id, data)

    @staticmethod
    def validate_stock(db: Session, pharmacy_id: str, batch_id: str, quantity: int) -> dict:
        batch = MedicineRepository.get_batch(db, batch_id)
        if not batch or batch.medicine.pharmacy_id != pharmacy_id:
            raise NotFoundException("MedicineBatch")

        if batch.status != "ACTIVE":
            raise ValidationException("Medicine batch is not active")

        if batch.expiry_date and batch.expiry_date < date.today():
            raise ValidationException("Medicine batch has expired")

        if batch.quantity_available < quantity:
            raise ValidationException("Insufficient stock")

        return {
            "success": True,
            "message": "Stock available",
            "batch": batch
        }
    @staticmethod
    def list_medicine_batches(db: Session, medicine_id: str) -> list[MedicineBatch]:
        return db.query(MedicineBatch).filter(MedicineBatch.medicine_id == medicine_id).order_by(MedicineBatch.expiry_date.asc()).all()
