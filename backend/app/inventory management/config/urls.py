from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ─── FIXED BULLETPROOF STRAP: Catch both with and without trailing slash patterns ───
    path('inventory/', include('inventory.urls')), 
    path('inventory', include('inventory.urls')), 
    
    # Global fallback escape layout hook
    path('', include('inventory.urls')), 
]
