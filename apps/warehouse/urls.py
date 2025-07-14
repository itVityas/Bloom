from django.urls import path

from apps.warehouse.views.type_of_work import (
    TypeOfWorkListCreateView,
    TypeOfWorkRetrieveUpdateDestroyView
)
from apps.warehouse.views.warehouse import (
    WarehouseListCreateView,
    WarehouseRetrieveUpdateDestroyView
)
from apps.warehouse.views.warehouse_action import (
    WarehouseActionCreateView,
    WarehouseActionListView,
    WarehouseActionRetrieveUpdateDestroyView,
    WarehouseActionRetrieveView
)
from apps.warehouse.views.pallet import (
    PalletListCreateAPIView,
    PalletRetrieveUpdateDestroyView
)

urlpatterns = [
    path('typeofwork/', TypeOfWorkListCreateView.as_view()),
    path('typeofwork/<int:pk>/', TypeOfWorkRetrieveUpdateDestroyView.as_view()),
    path('warehouse/', WarehouseListCreateView.as_view()),
    path('warehouse/<int:pk>/', WarehouseRetrieveUpdateDestroyView.as_view()),
    path('warehouseaction/create/', WarehouseActionCreateView.as_view()),
    path('warehouseaction/update/<int:pk>/', WarehouseActionRetrieveUpdateDestroyView.as_view()),
    path('warehouseaction/list/', WarehouseActionListView.as_view()),
    path('warehouseaction/detailed/<int:pk>/', WarehouseActionRetrieveView.as_view()),
    path('pallet/', PalletListCreateAPIView.as_view()),
    path('pallet/<int:pk>/', PalletRetrieveUpdateDestroyView.as_view()),
]
