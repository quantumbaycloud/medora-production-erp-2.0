import io
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, List
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.billing.models import Invoice, InvoiceItem
from app.purchase.models import PurchaseInvoice
from app.medicine.models import Medicine, MedicineBatch
from app.customer.models import Customer
from app.reports.schemas import (
    DashboardKPIResponse,
    SalesReportItem,
    ExpiryReportItem,
    GSTReportItem,
)

class ReportService:

    @staticmethod
    def get_dashboard_kpis(db: Session, pharmacy_id: str, branch_id: Optional[str] = None) -> DashboardKPIResponse:
        today = date.today()
        first_of_month = today.replace(day=1)

        # 1. Total Customers
        total_customers = db.query(func.count(Customer.id)).filter(Customer.pharmacy_id == pharmacy_id).scalar() or 0

        # 2. Total Medicines
        total_medicines = db.query(func.count(Medicine.id)).filter(Medicine.pharmacy_id == pharmacy_id).scalar() or 0

        # 3. Low Stock Count (batch quantity <= min_stock_level or <= 10)
        low_stock_q = (
            db.query(func.count(MedicineBatch.id))
            .join(Medicine, Medicine.id == MedicineBatch.medicine_id)
            .filter(
                Medicine.pharmacy_id == pharmacy_id,
                MedicineBatch.status == "ACTIVE",
                MedicineBatch.quantity_available <= Medicine.min_stock_level
            )
        )
        low_stock_count = low_stock_q.scalar() or 0

        # 4. Near Expiry / Expired Count (within next 30 days)
        expiry_threshold = today + timedelta(days=30)
        near_expiry_q = (
            db.query(func.count(MedicineBatch.id))
            .join(Medicine, Medicine.id == MedicineBatch.medicine_id)
            .filter(
                Medicine.pharmacy_id == pharmacy_id,
                MedicineBatch.status == "ACTIVE",
                MedicineBatch.expiry_date <= expiry_threshold
            )
        )
        near_expiry_count = near_expiry_q.scalar() or 0

        # 5. Sales metrics
        today_sales_q = db.query(func.sum(Invoice.total_amount)).filter(
            Invoice.pharmacy_id == pharmacy_id,
            func.date(Invoice.invoice_date) == today
        )
        monthly_sales_q = db.query(func.sum(Invoice.total_amount)).filter(
            Invoice.pharmacy_id == pharmacy_id,
            Invoice.invoice_date >= datetime.combine(first_of_month, datetime.min.time())
        )

        if branch_id:
            today_sales_q = today_sales_q.filter(Invoice.branch_id == branch_id)
            monthly_sales_q = monthly_sales_q.filter(Invoice.branch_id == branch_id)

        today_sales = Decimal(str(today_sales_q.scalar() or "0.00"))
        monthly_sales = Decimal(str(monthly_sales_q.scalar() or "0.00"))

        # 6. Purchase metrics
        today_purch_q = db.query(func.sum(PurchaseInvoice.total_amount)).filter(
            PurchaseInvoice.pharmacy_id == pharmacy_id,
            PurchaseInvoice.invoice_date == today
        )
        pending_purch_q = db.query(func.sum(PurchaseInvoice.total_amount)).filter(
            PurchaseInvoice.pharmacy_id == pharmacy_id,
            PurchaseInvoice.status == "DRAFT"
        )
        today_purchase = Decimal(str(today_purch_q.scalar() or "0.00"))
        pending_purchases = Decimal(str(pending_purch_q.scalar() or "0.00"))

        # 7. Customer outstanding payments
        outstanding_q = db.query(func.sum(Customer.outstanding_amount)).filter(Customer.pharmacy_id == pharmacy_id)
        outstanding_payments = Decimal(str(outstanding_q.scalar() or "0.00"))

        # Monthly profit calculation (Gross margin estimate from sales vs inventory purchase costs or standard margin)
        monthly_profit = (monthly_sales * Decimal("0.25")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return DashboardKPIResponse(
            today_sales=today_sales,
            today_purchase=today_purchase,
            monthly_sales=monthly_sales,
            monthly_profit=monthly_profit,
            total_customers=total_customers,
            total_medicines=total_medicines,
            low_stock_count=low_stock_count,
            near_expiry_count=near_expiry_count,
            outstanding_payments=outstanding_payments,
            pending_purchases=pending_purchases,
        )

    @staticmethod
    def generate_sales_report(
        db: Session,
        pharmacy_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        branch_id: Optional[str] = None,
        export_excel: bool = False,
    ):
        q = db.query(Invoice).filter(Invoice.pharmacy_id == pharmacy_id)
        if branch_id:
            q = q.filter(Invoice.branch_id == branch_id)
        if start_date:
            q = q.filter(func.date(Invoice.invoice_date) >= start_date)
        if end_date:
            q = q.filter(func.date(Invoice.invoice_date) <= end_date)

        invoices = q.order_by(Invoice.invoice_date.desc()).all()

        report_data = [
            SalesReportItem(
                invoice_number=inv.invoice_number,
                date=inv.invoice_date.strftime("%Y-%m-%d %H:%M"),
                customer_name=inv.customer_name,
                payment_method=inv.payment_method,
                total_amount=inv.total_amount,
                tax_amount=inv.tax_amount,
                discount_amount=inv.discount_amount,
                status=inv.payment_status,
            )
            for inv in invoices
        ]

        if not export_excel:
            return report_data

        data_dicts = [item.model_dump() for item in report_data]
        df = pd.DataFrame(data_dicts)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Sales_Report")
        output.seek(0)
        return output

    @staticmethod
    def generate_expiry_report(
        db: Session,
        pharmacy_id: str,
        days_ahead: int = 60,
        export_excel: bool = False,
    ):
        today = date.today()
        threshold = today + timedelta(days=days_ahead)

        records = (
            db.query(Medicine, MedicineBatch)
            .join(MedicineBatch, Medicine.id == MedicineBatch.medicine_id)
            .filter(
                Medicine.pharmacy_id == pharmacy_id,
                MedicineBatch.status == "ACTIVE",
                MedicineBatch.expiry_date <= threshold
            )
            .order_by(MedicineBatch.expiry_date.asc())
            .all()
        )

        report_data = []
        for med, batch in records:
            status_str = "Expired" if batch.expiry_date < today else "Near Expiry"
            report_data.append(
                ExpiryReportItem(
                    medicine_name=med.name,
                    generic_name=med.generic_name,
                    batch_number=batch.batch_number,
                    expiry_date=str(batch.expiry_date),
                    stock_available=batch.quantity_available,
                    selling_price=batch.selling_price,
                    status=status_str,
                )
            )

        if not export_excel:
            return report_data

        data_dicts = [item.model_dump() for item in report_data]
        df = pd.DataFrame(data_dicts)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Expiry_Report")
        output.seek(0)
        return output

    @staticmethod
    def generate_gst_report(
        db: Session,
        pharmacy_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        export_excel: bool = False,
    ):
        q = (
            db.query(InvoiceItem, Invoice, Medicine)
            .join(Invoice, Invoice.id == InvoiceItem.invoice_id)
            .join(Medicine, Medicine.id == InvoiceItem.medicine_id)
            .filter(Invoice.pharmacy_id == pharmacy_id)
        )
        if start_date:
            q = q.filter(func.date(Invoice.invoice_date) >= start_date)
        if end_date:
            q = q.filter(func.date(Invoice.invoice_date) <= end_date)

        rows = q.all()

        report_data = []
        for item, inv, med in rows:
            taxable_val = (item.total_amount - item.gst_amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            half_gst = (item.gst_amount / Decimal("2")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            report_data.append(
                GSTReportItem(
                    hsn_code=med.hsn_code,
                    medicine_name=item.medicine_name,
                    taxable_value=taxable_val,
                    gst_percentage=item.gst_percentage,
                    cgst_amount=half_gst,
                    sgst_amount=half_gst,
                    total_gst=item.gst_amount,
                )
            )

        if not export_excel:
            return report_data

        data_dicts = [item.model_dump() for item in report_data]
        df = pd.DataFrame(data_dicts)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="GST_Report")
        output.seek(0)
        return output
