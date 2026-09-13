import requests
from django.db import models
from medicine.models import Medicine

class Inventory(models.Model):
    class Meta:
        verbose_name_plural = "Inventories"
    medicine = models.OneToOneField(Medicine, on_delete=models.CASCADE)
    current_stock = models.IntegerField(default=0)
    opening_stock = models.IntegerField(default=0)
    closing_stock = models.IntegerField(default=0)
    opening_period_start = models.DateField(null=True, blank=True)
    closing_period_end = models.DateField(null=True, blank=True)
    reserved_stock = models.IntegerField(default=0)
    warehouse = models.CharField(max_length=100, default="Main Warehouse")
    rack_number = models.CharField(max_length=50, default="A1")


    @property
    def available_stock(self):
        return self.current_stock - self.reserved_stock
    
    def __str__(self):
        return self.medicine.medicine_name

class StockTransfer(models.Model):
    soruce_branch = models.CharField(max_length=100)
    destination_branch = models.CharField(max_length=100)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    transfer_date = models.DateField()
    status = models.CharField(max_length=20)
    transferred_by = models.CharField(max_length=100, default="System Operator", null=True, blank=True)

    def __str__(self):
        return f"{self.medicine} - {self.quantity}"
    
class physicalStockVerification(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    system_stock = models.IntegerField()
    actual_stock = models.IntegerField()
    verfication_date = models.DateField()
    verified_by = models.CharField(max_length=100, default="System Inspector", null=True, blank=True)

class DamagedStock(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    batch = models.ForeignKey('batch.Batch', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    reason = models.CharField(max_length=200)
    reported_by = models.CharField(max_length=100, default="Store Manager", null=True, blank=True)

class ExpiredStock(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    batch = models.ForeignKey('batch.Batch', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    expiry_date = models.DateField()

class NearExpiryStock(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE) 
    batch = models.ForeignKey('batch.Batch', on_delete=models.CASCADE)
    expiry_date = models.DateField()
    alert_days = models.IntegerField(default=90)

class LowStockAlert(models.Model):
    medicine =  models.ForeignKey(Medicine, on_delete=models.CASCADE)
    current_stock = models.IntegerField()
    minimum_stock = models.IntegerField()

class OverStockAlert(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    current_stock = models.IntegerField()
    maximum_stock = models.IntegerField()

class StockLedger(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=30)
    quantity = models.IntegerField()
    previous_stock = models.IntegerField()
    new_stock = models.IntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # 1. Determine if this is a newly created transaction
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # ─── INTEGRATED: AUTOMATED EMAIL THRESHOLD SYSTEM ───────────────────
        from django.core.mail import send_mail
        
        min_threshold = int(getattr(self.medicine, 'minimum_stock_level', 10) or 10)
        ideal_max = min_threshold * 1000  # Ceiling capacity limit

        # Condition A: Critical Deficit Bound Crossed
        if self.new_stock <= min_threshold:
            LowStockAlert.objects.get_or_create(
                medicine=self.medicine,
                current_stock=self.new_stock,
                minimum_stock=min_threshold
            )
            
            # Send real-time terminal alert
            send_mail(
                subject=f"🚨 CRITICAL LOW STOCK: {self.medicine.medicine_name}",
                message=(
                    f"Deficit threshold crossed via transaction action.\n\n"
                    f"Medicine: {self.medicine.medicine_name}\n"
                    f"Current Balance: {self.new_stock} units\n"
                    f"Safety Level: {min_threshold} units\n"
                ),
                from_email=None,
                recipient_list=['inventory-manager@medorax.com'],
                fail_silently=True
            )

        # Condition B: High Excess Bound Crossed
        elif self.new_stock > ideal_max:
            OverStockAlert.objects.get_or_create(
                medicine=self.medicine,
                current_stock=self.new_stock,
                maximum_stock=ideal_max
            )

            # Send real-time terminal alert
            send_mail(
                subject=f"⚠️ WAREHOUSE OVERSTOCK ALERT: {self.medicine.medicine_name}",
                message=(
                    f"Surplus saturation ceiling crossed via transaction action.\n\n"
                    f"Medicine: {self.medicine.medicine_name}\n"
                    f"Current Balance: {self.new_stock:,} units\n"
                    f"Ideal Max: {ideal_max:,} units\n"
                ),
                from_email=None,
                recipient_list=['inventory-manager@medorax.com'],
                fail_silently=True
            )
        # ───────────────────────────────────────────────────────────────────
            
        # 3. Inter-Service Communication: Send Data to Financial System
        if is_new and self.transaction_type.lower() in ['sale', 'restock']:
            try:
                total_value = float(self.medicine.price) * self.quantity
                payload = {
                    "medicine_name": self.medicine.medicine_name,
                    "transaction_type": self.transaction_type.lower(),
                    "quantity": self.quantity,
                    "total_amount": total_value
                }
                finance_url = "http://127.0.0.1:8000/api/webhooks/internal/inventory-sync" 
                response = requests.post(finance_url, json=payload, timeout=5)
                response.raise_for_status()
            except Exception as e:
                print(f"Failed to sync with financial system: {e}")
