from django.db import models

class Supplier(models.Model):
    supplier_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()

    gst = models.CharField(max_length=20)
    drug_license = models.CharField(max_length=50)

    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=30)
    ifsc_code = models.CharField(max_length=20)

    payment_terms = models.CharField(max_length=100)

    def __str__(self):
        return self.supplier_name
    
    @property
    def outstanding_balance(self):
        total_purchase = sum(
            invoice.total_amount for invoice in self.purchaseinvoice_set.all()
        )
        total_paid = sum(
            invoice.paid_amount for invoice in self.purchaseinvoice_set.all()
        )
        return total_purchase - total_paid
    
class SupplierLedger(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    transaction_date = models.DateField()
    transaction_type = models.CharField(max_length=30)
    reference_number = models.CharField(max_length=50)
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.supplier.supplier_name} - {self.reference_number}"