import io
import pandas as pd
from sqlalchemy.orm import Session
from fastapi import HTTPException
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from app.medicine.models import Medicine, MedicineBatch
from app.supplier.models import Supplier
from app.inventory.models import InventoryLedger

class ExportService:

    @staticmethod
    def get_dataframe(db: Session, pharmacy_id: str, entity: str) -> pd.DataFrame:
        if entity == "medicines":
            records = (
                db.query(Medicine, MedicineBatch)
                .outerjoin(MedicineBatch, Medicine.id == MedicineBatch.medicine_id)
                .filter(Medicine.pharmacy_id == pharmacy_id)
                .all()
            )
            data = []
            for med, batch in records:
                row = {
                    "Medicine ID": med.id,
                    "Name": med.name,
                    "Generic Name": med.generic_name or "",
                    "Manufacturer": med.manufacturer or "",
                    "Category": med.category or "",
                    "Barcode": med.barcode or "",
                    "SKU": med.sku or "",
                    "Batch Number": batch.batch_number if batch else "",
                    "Expiry Date": str(batch.expiry_date) if batch else "",
                    "Stock Available": batch.quantity_available if batch else 0,
                    "Purchase Price": float(batch.purchase_price) if batch else 0.0,
                    "Selling Price": float(batch.selling_price) if batch else 0.0,
                    "MRP": float(batch.mrp) if batch else 0.0,
                }
                data.append(row)
            return pd.DataFrame(data)

        elif entity == "ledger":
            records = (
                db.query(InventoryLedger)
                .filter(InventoryLedger.pharmacy_id == pharmacy_id)
                .order_by(InventoryLedger.created_at.desc())
                .all()
            )
            data = [
                {
                    "ID": r.id,
                    "Medicine ID": r.medicine_id,
                    "Batch Number": r.batch_number,
                    "Type": r.transaction_type,
                    "Quantity": r.quantity,
                    "Reference ID": r.reference_id or "",
                    "Notes": r.notes or "",
                    "Timestamp": str(r.created_at),
                }
                for r in records
            ]
            return pd.DataFrame(data)

        elif entity == "suppliers":
            records = db.query(Supplier).filter(Supplier.pharmacy_id == pharmacy_id).all()
            data = [
                {
                    "ID": s.id,
                    "Name": s.name,
                    "Contact Person": s.contact_person or "",
                    "Phone": s.phone or "",
                    "Email": s.email or "",
                    "GSTIN": s.gstin or "",
                    "Address": s.address or "",
                }
                for s in records
            ]
            return pd.DataFrame(data)

        else:
            raise HTTPException(status_code=400, detail=f"Unsupported entity for export: '{entity}'")

    @staticmethod
    def export_csv(df: pd.DataFrame) -> io.BytesIO:
        buffer = io.BytesIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        return buffer

    @staticmethod
    def export_excel(df: pd.DataFrame) -> io.BytesIO:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Data Export")
        buffer.seek(0)
        return buffer

    @staticmethod
    def export_pdf(df: pd.DataFrame, title: str = "MEDORAX DATA REPORT") -> io.BytesIO:
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Header
        p.setFont("Helvetica-Bold", 16)
        p.setFillColor(colors.HexColor("#1A365D"))
        p.drawString(50, height - 50, title)

        p.setFont("Helvetica", 10)
        p.setFillColor(colors.HexColor("#4A5568"))
        p.drawString(50, height - 70, f"Generated automatically by Medorax ERP. Total Rows: {len(df)}")
        p.setStrokeColor(colors.HexColor("#CBD5E0"))
        p.setLineWidth(1)
        p.line(50, height - 80, width - 50, height - 80)

        # Table data
        y = height - 110
        p.setFont("Helvetica-Bold", 8)
        p.setFillColor(colors.black)

        columns = list(df.columns)[:7]  # Print first 7 columns for width
        col_width = (width - 100) / len(columns)

        for i, col in enumerate(columns):
            p.drawString(50 + (i * col_width), y, str(col)[:15])

        y -= 15
        p.line(50, y + 5, width - 50, y + 5)
        p.setFont("Helvetica", 7)

        for _, row in df.iterrows():
            if y < 50:
                p.showPage()
                y = height - 50
                p.setFont("Helvetica", 7)

            for i, col in enumerate(columns):
                val_str = str(row[col])[:18]
                p.drawString(50 + (i * col_width), y, val_str)
            y -= 14

        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer
