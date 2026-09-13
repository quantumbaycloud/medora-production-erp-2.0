from django.db import models
from datetime import date
from medicine.models import Medicine

class Batch(models.Model):

    class Meta:
        verbose_name_plural = "batches"
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Near Expiry', 'Near Expiry'),
        ('Expired', 'Expired'),
    ]
    batch_number = models.CharField(max_length=50, unique=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    manufacturing_date = models.DateField()
    expiry_date = models.DateField()
    batch_quantity = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    
    @property
    def is_expired(self):
        return self.expiry_date < date.today()
    
    @property
    def is_near_expiry(self):
        return 0 <= (self.expiry_date - date.today()).days <= 30
    
    def save(self, *args, **kwargs):
        if self.expiry_date < date.today():
            self.status = "Expired"
        elif 0 <= (self.expiry_date - date.today()).days <=30:
            self.status = "Near Expiry"
        else:
            self.status = "Available"
        super().save(*args, **kwargs)
    
    
    
    def __str__(self):
        return f"{self.medicine.medicine_name} - {self.batch_number}"
