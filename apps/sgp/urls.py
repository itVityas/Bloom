from django.urls import path

from apps.sgp.views.consignment import ConsignmentCreateView
from apps.sgp.views.storage_limist import (
    StorageLimitsCreateView, StorageLimitsRUDView, StorageLimitsListView)
from apps.sgp.views.shipment_bans import (
    ShipmentBansCreateView, ShipmentBansRUDView, ShipmentBansListView, ShipmentBansGetView
)


urlpatterns = [
    path('consignment/', ConsignmentCreateView.as_view()),

    # StorageLimits
    path('storage-limits/', StorageLimitsListView.as_view()),
    path('storage-limits/create/', StorageLimitsCreateView.as_view()),
    path('storage-limits/<int:pk>/', StorageLimitsRUDView.as_view()),

    # Shipment Bans
    path('shipment-bans/', ShipmentBansListView.as_view()),
    path('shipment-bans/create/', ShipmentBansCreateView.as_view()),
    path('shipment-bans/<int:pk>/', ShipmentBansRUDView.as_view()),
    path('shipment-bans/get/<int:pk>/', ShipmentBansGetView.as_view()),
]
