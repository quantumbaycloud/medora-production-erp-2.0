from django.apps import AppConfig

class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'

    # ─── FORCE DJANGO TO INITIALIZE THE SIGNAL ALERTS ───────────────────────
    def ready(self):
        # Importing inside the ready() hook prevents circular import bugs
        import inventory.views 
    # ────────────────────────────────────────────────────────────────────────
