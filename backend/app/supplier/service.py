from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.exceptions import NotFoundException
from app.catalog.models import CatalogOption
from app.supplier.models import Supplier
from app.supplier.repository import SupplierRepository
from app.supplier.schemas import SupplierCreate, SupplierUpdate

class SupplierService:
    @staticmethod
    def _validate_category(db: Session, pharmacy_id: str, category_id: str | None):
        if not category_id:
            return
        category = db.query(CatalogOption).filter(
            CatalogOption.id == category_id,
            CatalogOption.pharmacy_id == pharmacy_id,
            CatalogOption.option_type == "supplier_category",
            CatalogOption.is_active.is_(True),
        ).first()
        if not category:
            raise HTTPException(422, "Invalid or inactive supplier category for this pharmacy")

    @staticmethod
    def create_supplier(db: Session, pharmacy_id: str, data: SupplierCreate) -> Supplier:
        SupplierService._validate_category(db, pharmacy_id, data.category_id)
        return SupplierRepository.create_supplier(db, pharmacy_id, data)

    @staticmethod
    def get_supplier(db: Session, pharmacy_id: str, supplier_id: str) -> Supplier:
        supplier = SupplierRepository.get_supplier(db, pharmacy_id, supplier_id)
        if not supplier:
            raise NotFoundException("Supplier")
        return supplier

    @staticmethod
    def list_suppliers(db: Session, pharmacy_id: str, query: str = None) -> list[Supplier]:
        return SupplierRepository.get_suppliers(db, pharmacy_id, query)

    @staticmethod
    def update_supplier(db: Session, pharmacy_id: str, supplier_id: str, data: SupplierUpdate) -> Supplier:
        SupplierService._validate_category(db, pharmacy_id, data.category_id)
        supplier = SupplierService.get_supplier(db, pharmacy_id, supplier_id)
        return SupplierRepository.update_supplier(db, supplier, data)

    @staticmethod
    def delete_supplier(db: Session, pharmacy_id: str, supplier_id: str) -> None:
        supplier = SupplierService.get_supplier(db, pharmacy_id, supplier_id)
        SupplierRepository.delete_supplier(db, supplier)
