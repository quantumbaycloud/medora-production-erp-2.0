import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from app.billing.models import Invoice

class PrintService:

    @staticmethod
    def generate_thermal_receipt(invoice: Invoice, pharmacy_name: str = "Medorax Pharmacy") -> str:
        """
        Generate plain text receipt for 80mm thermal printers (48 column standard)
        """
        divider = "-" * 48
        lines = [
            f"{pharmacy_name.center(48)}",
            f"Tax Invoice: {invoice.invoice_number}".center(48),
            f"Date: {invoice.invoice_date.strftime('%d-%b-%Y %H:%M')}".center(48),
            f"Customer: {invoice.customer_name or 'Walk-in'}".center(48),
            divider,
            f"{'Item':<20} {'Qty':<5} {'Rate':<10} {'Amount':>10}",
            divider,
        ]

        for item in invoice.items:
            name = item.medicine_name[:19]
            qty = str(item.quantity)
            rate = f"{float(item.rate):.2f}"
            amt = f"{float(item.total_amount):.2f}"
            lines.append(f"{name:<20} {qty:<5} {rate:<10} {amt:>10}")

        lines.extend([
            divider,
            f"{'Subtotal:':<35} {float(invoice.total_amount - invoice.tax_amount + invoice.discount_amount):>11.2f}",
            f"{'Discount:':<35} -{float(invoice.discount_amount):>10.2f}",
            f"{'Tax (GST):':<35} {float(invoice.tax_amount):>11.2f}",
            divider,
            f"{'GRAND TOTAL:':<35} {float(invoice.total_amount):>11.2f}",
            f"{'Payment Method:':<35} {invoice.payment_method:>11}",
            f"{'Payment Status:':<35} {invoice.payment_status:>11}",
            divider,
            f"{'Thank you for your visit!':^48}",
            f"{'Medicines cannot be returned without bill':^48}",
            "\n\n\n\x1dV\x00"  # Paper cut command for ESC/POS
        ])

        return "\n".join(lines)

    @staticmethod
    def generate_a4_pdf(invoice: Invoice, pharmacy_name: str = "Medorax Pharmacy") -> io.BytesIO:
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Header
        p.setFont("Helvetica-Bold", 18)
        p.setFillColor(colors.HexColor("#1A365D"))
        p.drawString(50, height - 50, pharmacy_name)

        p.setFont("Helvetica-Bold", 12)
        p.setFillColor(colors.HexColor("#4A5568"))
        p.drawRightString(width - 50, height - 50, "TAX INVOICE")

        p.setFont("Helvetica", 9)
        p.drawRightString(width - 50, height - 65, f"Invoice #: {invoice.invoice_number}")
        p.drawRightString(width - 50, height - 78, f"Date: {invoice.invoice_date.strftime('%d-%m-%Y %H:%M')}")

        p.drawString(50, height - 75, f"Customer: {invoice.customer_name or 'Walk-in Customer'}")
        p.drawString(50, height - 88, f"Payment Method: {invoice.payment_method} ({invoice.payment_status})")

        p.setStrokeColor(colors.HexColor("#CBD5E0"))
        p.line(50, height - 100, width - 50, height - 100)

        # Table header
        y = height - 120
        p.setFont("Helvetica-Bold", 9)
        p.drawString(50, y, "#")
        p.drawString(70, y, "Medicine Description")
        p.drawString(240, y, "Batch")
        p.drawString(310, y, "Qty")
        p.drawString(360, y, "Rate")
        p.drawString(420, y, "GST")
        p.drawRightString(width - 50, y, "Amount")

        p.line(50, y - 5, width - 50, y - 5)
        p.setFont("Helvetica", 9)

        y -= 20
        for idx, item in enumerate(invoice.items, 1):
            if y < 100:
                p.showPage()
                y = height - 50
                p.setFont("Helvetica", 9)

            p.drawString(50, y, str(idx))
            p.drawString(70, y, item.medicine_name[:30])
            p.drawString(240, y, item.batch_number[:10])
            p.drawString(310, y, str(item.quantity))
            p.drawString(360, y, f"{float(item.rate):.2f}")
            p.drawString(420, y, f"{float(item.gst_percentage):.1f}%")
            p.drawRightString(width - 50, y, f"{float(item.total_amount):.2f}")
            y -= 18

        p.line(50, y, width - 50, y)
        y -= 20

        # Totals box
        p.setFont("Helvetica-Bold", 10)
        p.drawRightString(width - 150, y, "Total Discount:")
        p.drawRightString(width - 50, y, f"-{float(invoice.discount_amount):.2f}")
        y -= 15
        p.drawRightString(width - 150, y, "Total Tax (GST):")
        p.drawRightString(width - 50, y, f"{float(invoice.tax_amount):.2f}")
        y -= 18
        p.setFont("Helvetica-Bold", 12)
        p.drawRightString(width - 150, y, "GRAND TOTAL:")
        p.drawRightString(width - 50, y, f"Rs. {float(invoice.total_amount):.2f}")

        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer
