import json
from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.catalog.models import CatalogOption
from app.catalog.schemas import CatalogOptionCreate, CatalogOptionUpdate

class CatalogService:
    @staticmethod
    def list(db: Session, pharmacy_id: str, option_type: str | None = None, active_only: bool = True):
        q = db.query(CatalogOption).filter(CatalogOption.pharmacy_id == pharmacy_id)
        if option_type:
            q = q.filter(CatalogOption.option_type == option_type)
        if active_only:
            q = q.filter(CatalogOption.is_active.is_(True))
        return q.order_by(CatalogOption.sort_order.asc(), CatalogOption.name.asc()).all()

    @staticmethod
    def create(db: Session, pharmacy_id: str, data: CatalogOptionCreate):
        code = data.code.strip().lower().replace(" ", "-")
        if not code:
            raise HTTPException(422, "Catalog code is required")
        exists = db.query(CatalogOption).filter(
            CatalogOption.pharmacy_id == pharmacy_id,
            CatalogOption.option_type == data.option_type,
            CatalogOption.code == code,
        ).first()
        if exists:
            raise HTTPException(409, "This option already exists")
        row = CatalogOption(
            pharmacy_id=pharmacy_id, option_type=data.option_type.strip(),
            code=code, name=data.name.strip(), is_active=data.is_active,
            sort_order=data.sort_order,
            metadata_json=json.dumps(data.metadata, separators=(",", ":"), sort_keys=True) if data.metadata else None,
        )
        db.add(row); db.flush()
        return row

    @staticmethod
    def update(db: Session, pharmacy_id: str, option_id: str, data: CatalogOptionUpdate):
        row = db.query(CatalogOption).filter(CatalogOption.id == option_id, CatalogOption.pharmacy_id == pharmacy_id).first()
        if not row:
            raise HTTPException(404, "Catalog option not found")
        values = data.model_dump(exclude_unset=True)
        if "metadata" in values:
            values["metadata_json"] = json.dumps(values.pop("metadata"), separators=(",", ":"), sort_keys=True) if values["metadata"] else None
        for key, value in values.items():
            setattr(row, key, value)
        db.flush()
        return row

    @staticmethod
    def delete(db: Session, pharmacy_id: str, option_id: str):
        row = db.query(CatalogOption).filter(CatalogOption.id == option_id, CatalogOption.pharmacy_id == pharmacy_id).first()
        if not row:
            raise HTTPException(404, "Catalog option not found")
        db.delete(row); db.flush()

    @staticmethod
    def as_dict(row):
        return {
            "id": row.id, "pharmacy_id": row.pharmacy_id, "option_type": row.option_type,
            "code": row.code, "name": row.name, "is_active": row.is_active,
            "sort_order": row.sort_order,
            "metadata": json.loads(row.metadata_json) if row.metadata_json else None,
            "created_at": row.created_at, "updated_at": row.updated_at,
        }
