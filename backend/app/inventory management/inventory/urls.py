from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from supplier.views import SupplierViewSet

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet, basename='supplier')

urlpatterns = [
    # ─── HIGH PRIORITY STANDALONE ROUTE ALIGNMENT ───
    # Points exactly to the newly added view function name
    path('live-stock-balance/', views.dedicated_available_stock_api, name='dedicated-available-stock'),
    path('available-stock/', views.dedicated_available_stock_api, name='available-stock-list-slash'),
    path('available-stock', views.dedicated_available_stock_api, name='available-stock-list-raw'),
    path('medicines/', views.dedicated_available_stock_api, name='medicines-list'),
    path('batches/', views.batch_management_api, name='batch-management'),

    # Excel Report Utility
    path('medicines/export-excel/', views.export_medicines_excel, name='export-medicines-excel'),
    path('medicines/<int:medicine_id>/batches/', views.medicine_batches_api, name='medicine-batches'),
    path('medicines/<int:pk>/', views.inventory_detail_api, name='medicines-detail'),
    
    # Inventory Lifecycle and Tracking
    path('opening-stock/', views.opening_stock_list_create, name='opening-stock'),
    path('closing-stock/', views.closing_stock_list_create, name='closing-stock'),
    path('reserved-stock/', views.reserved_stock_api, name='reserved-stock'),
    path('adjust/', views.adjust_stock_api, name='stock-adjustment-api'),
    path('transfers/', views.stock_transfer_api, name='stock-transfers-api'),
    path('verify-stock/', views.physical_verification_api, name='physical-verification-api'),
    path('damaged-stock/', views.damaged_stock_api, name='damaged-stock-api'),
    path('expired-stock/', views.expired_stock_api, name='expired-stock-api'),
    
    # Reports and Management Alerts
    path('reports/expiry/', views.near_expiry_report_api, name='near-expiry-report-api'),
    path('alerts/low-stock/', views.low_stock_alerts_api, name='low-stock-alerts-api'),
    path('alerts/overstock/', views.overstock_alerts_api, name='overstock-alerts-api'), 
    path('ledger/', views.stock_ledger_api, name='stock-ledger-api'),
    path('inventory/<int:pk>/', views.inventory_detail_api, name='inventory-detail'),
    
    # Router viewsets at the absolute bottom
    path('', include(router.urls)),
]
