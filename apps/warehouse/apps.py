from django.apps import AppConfig


class WarehouseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.warehouse'

    def ready(self):
        from apps.warehouse.signals.warehouse_product import WarehouseProductSignal