from django.db import models

class Medicine(models.Model):
    medicine_name = models.CharField(max_length=255)
    minimum_stock_level = models.IntegerField(default=10)
    
    # Financial and Tracking Fields
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True) 
    
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.medicine_name