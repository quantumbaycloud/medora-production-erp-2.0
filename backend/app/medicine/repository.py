from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.medicine.models import Medicine, MedicineBatch
from app.medicine.schemas import MedicineCreate, MedicineUpdate, MedicineBatchCreate, MedicineBatchUpdate

class MedicineRepository:
    
    @staticmethod
    def create_medicine(db: Session, pharmacy_id: str, data: MedicineCreate) -> Medicine:
        medicine = Medicine(**data.model_dump(), pharmacy_id=pharmacy_id)
        db.add(medicine)
        db.flush()
        return medicine

    @staticmethod
    def get_medicine(db: Session, pharmacy_id: str, medicine_id: str) -> Medicine | None:
        return db.query(Medicine).options(joinedload(Medicine.batches)).filter(
            Medicine.id == medicine_id, 
            Medicine.pharmacy_id == pharmacy_id
        ).first()

    @staticmethod
    def get_medicine_by_barcode(db: Session, pharmacy_id: str, barcode: str) -> Medicine | None:
        return db.query(Medicine).options(joinedload(Medicine.batches)).filter(
            Medicine.barcode == barcode, 
            Medicine.pharmacy_id == pharmacy_id
        ).first()

    @staticmethod
    def search_medicines(db: Session, pharmacy_id: str, query: str = None) -> list[Medicine]:
        q = db.query(Medicine).options(joinedload(Medicine.batches)).filter(Medicine.pharmacy_id == pharmacy_id)
        if query:
            q = q.filter(
                or_(
                    Medicine.name.ilike(f"%{query}%"),
                    Medicine.generic_name.ilike(f"%{query}%"),
                    Medicine.barcode == query,
                    Medicine.sku == query,
                )
            )
        return q.all()

    @staticmethod
    def update_medicine(db: Session, medicine: Medicine, data: MedicineUpdate) -> Medicine:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(medicine, key, value)
        db.flush()
        return medicine

    @staticmethod
    def create_batch(db: Session, medicine_id: str, data: MedicineBatchCreate) -> MedicineBatch:
        batch = MedicineBatch(**data.model_dump(), medicine_id=medicine_id)
        db.add(batch)
        db.flush()
        return batch

    @staticmethod
    def get_batch(db: Session, batch_id: str) -> MedicineBatch | None:
        return db.query(MedicineBatch).filter(MedicineBatch.id == batch_id).first()

    @staticmethod
    def update_batch(db: Session, batch: MedicineBatch, data: MedicineBatchUpdate) -> MedicineBatch:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(batch, key, value)
        db.flush()
        return batch
