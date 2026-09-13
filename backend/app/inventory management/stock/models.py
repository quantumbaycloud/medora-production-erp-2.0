from django.db import models
from medicine.models import Medicine
from django.contrib.auth.models import User

class StockAdjustment(models.Model):
    REASON_CHOICES = [
        ('Physical count', 'Physical count'),
        ('Damage', 'Damage'),
        ('Theft', 'Theft'),
        ('Missing Stock', 'Missing Stock'),
        ('Manual Correction', 'Manual Correction'),
    ]

    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    old_quantity = models.IntegerField()
    new_quantity = models.IntegerField()
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine.medicine_name} - {self.reason}"


