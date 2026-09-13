from django.contrib import admin
from .models import (
    Inventory,
    StockTransfer,
    physicalStockVerification,
    DamagedStock,
    ExpiredStock,
    NearExpiryStock,
    LowStockAlert,
    OverStockAlert,
    StockLedger,
)

admin.site.register(Inventory)
admin.site.register(StockTransfer)
admin.site.register(physicalStockVerification)
admin.site.register(DamagedStock)
admin.site.register(ExpiredStock)
admin.site.register(NearExpiryStock)
admin.site.register(LowStockAlert)
admin.site.register(OverStockAlert)
admin.site.register(StockLedger)

