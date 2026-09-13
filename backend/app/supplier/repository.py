from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.supplier.models import Supplier
from app.supplier.schemas import SupplierCreate, SupplierUpdate

class SupplierRepository:

    @staticmethod
    def create_supplier(db: Session, pharmacy_id: str, data: SupplierCreate) -> Supplier:
        supplier = Supplier(**data.model_dump(exclude={"pharmacy_id"}), pharmacy_id=pharmacy_id)
        db.add(supplier)
        db.flush()
        return supplier

    @staticmethod
    def get_supplier(db: Session, pharmacy_id: str, supplier_id: str) -> Supplier | None:
        return db.query(Supplier).filter(
            Supplier.id == supplier_id,
            Supplier.pharmacy_id == pharmacy_id
        ).first()

    @staticmethod
    def get_suppliers(db: Session, pharmacy_id: str, query: str = None) -> list[Supplier]:
        q = db.query(Supplier).filter(Supplier.pharmacy_id == pharmacy_id)
        if query:
            q = q.filter(
                or_(
                    Supplier.name.ilike(f"%{query}%"),
                    Supplier.contact_person.ilike(f"%{query}%"),
                    Supplier.phone.ilike(f"%{query}%"),
                    Supplier.gstin.ilike(f"%{query}%"),
                )
            )
        return q.order_by(Supplier.name.asc()).all()

    @staticmethod
    def update_supplier(db: Session, supplier: Supplier, data: SupplierUpdate) -> Supplier:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(supplier, key, value)
        db.flush()
        return supplier

    @staticmethod
    def delete_supplier(db: Session, supplier: Supplier) -> None:
        db.delete(supplier)
        db.flush()
