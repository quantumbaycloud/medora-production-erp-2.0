from rest_framework import serializers
from .models import Inventory

class InventorySerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.medicine_name', read_only=True)
    medicine_sku = serializers.CharField(source='medicine.sku', read_only=True)
    medicine_price = serializers.DecimalField(source='medicine.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'