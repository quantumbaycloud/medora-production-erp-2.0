import io
from datetime import datetime
from decimal import Decimal
import pandas as pd
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

from app.medicine.models import Medicine, MedicineBatch
from app.inventory.schemas import ImportSummaryResponse

class ImportService:

    @staticmethod
    def import_medicines_csv(db: Session, pharmacy_id: str, file: UploadFile) -> ImportSummaryResponse:
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Invalid file format. Only CSV files are supported.")

        try:
            content = file.file.read()
            df = pd.read_csv(io.BytesIO(content))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse CSV file: {str(e)}")

        required_cols = {"name", "batch_number", "expiry_date", "purchase_price", "selling_price", "mrp", "quantity"}
        missing_cols = required_cols - set(df.columns)
        if missing_cols:
            raise HTTPException(
                status_code=400,
                detail=f"CSV missing required columns: {list(missing_cols)}"
            )

        total_processed = 0
        successful = 0
        failed = 0
        errors = []

        for index, row in df.iterrows():
            total_processed += 1
            try:
                # Find or create medicine
                med_name = str(row["name"]).strip()
                medicine = (
                    db.query(Medicine)
                    .filter(Medicine.pharmacy_id == pharmacy_id, Medicine.name.ilike(med_name))
                    .first()
                )
                if not medicine:
                    medicine = Medicine(
                        pharmacy_id=pharmacy_id,
                        name=med_name,
                        generic_name=str(row.get("generic_name", "")) or None,
                        manufacturer=str(row.get("manufacturer", "")) or None,
                        category=str(row.get("category", "")) or None,
                        barcode=str(row.get("barcode", "")) if pd.notna(row.get("barcode")) else None,
                        sku=str(row.get("sku", "")) if pd.notna(row.get("sku")) else None,
                    )
                    db.add(medicine)
                    db.flush()

                # Parse expiry date
                expiry_str = str(row["expiry_date"]).strip()
                try:
                    expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
                except ValueError:
                    expiry_date = datetime.strptime(expiry_str, "%d-%m-%Y").date()

                batch_num = str(row["batch_number"]).strip()
                batch = (
                    db.query(MedicineBatch)
                    .filter(
                        MedicineBatch.medicine_id == medicine.id,
                        MedicineBatch.batch_number == batch_num
                    )
                    .first()
                )

                qty = int(row["quantity"])
                p_price = Decimal(str(row["purchase_price"]))
                s_price = Decimal(str(row["selling_price"]))
                mrp_val = Decimal(str(row["mrp"]))

                if batch:
                    batch.quantity_available += qty
                    batch.purchase_price = p_price
                    batch.selling_price = s_price
                    batch.mrp = mrp_val
                    batch.expiry_date = expiry_date
                else:
                    batch = MedicineBatch(
                        medicine_id=medicine.id,
                        batch_number=batch_num,
                        expiry_date=expiry_date,
                        purchase_price=p_price,
                        selling_price=s_price,
                        mrp=mrp_val,
                        quantity_available=qty,
                        status="ACTIVE",
                    )
                    db.add(batch)

                successful += 1
            except Exception as e:
                failed += 1
                errors.append(f"Row {index + 1}: {str(e)}")

        db.flush()
        return ImportSummaryResponse(
            status="Complete",
            total_processed=total_processed,
            successful=successful,
            failed=failed,
            errors=errors[:20]  # Cap error list
        )
