from django.db import models
from supplier.models import Supplier
from medicine.models import Medicine

class PurchaseOrder(models.Model):

    STATUS = (
        ('Draft', 'Draft'),
        ('Approved', 'Approved'),
        ('Cancelled', 'Cancelled'),
    )

    po_number = models.CharField(max_length=20, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order_date = models.DateField()
    expected_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS, default='Draft')

    def __str__(self):
        return self.po_number

class PurchaseOrderItem(models.Model):

    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

class PurchaseInvoice(models.Model):
    invoice_number = models.CharField(max_length=30)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    invoice_date = models.DateField()
class GoodReceipt(models.Model):
    Purchaseinvoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    received_qty = models.IntegerField()

class PurchaseReturn(models.Model):
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    return_qty = models.IntegerField()
    reason = models.TextField()

class CreditNote(models.Model):
    purchase_return = models.ForeignKey(PurchaseReturn, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
