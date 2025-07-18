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
from apps.warehouse.views.warehouse_products import (
    WarehouseProductCreateAPIView,
    WarehouseProductListAPIView,
    WarehouseProductRetrieveAPIView,
    WarehouseProductRetrieveUpdateDestroyView,
    WarehouseProductCreateByBarcodeAPIView,
)
from apps.warehouse.views.palleting import (
    PalletingCreateAPIView,
    PalletingListAPIView,
    PalletingRetrieveAPIView,
    PalletingRetrieveUpdateDestroyAPIView
)
from apps.warehouse.views.warehouse_ttn import (
    WarehouseTTNListCreateAPIView,
    WarehouseTTNRetrieveUpdateDestroyAPIView,
    WarehouseTTNByUserIdAPIView
)
from apps.warehouse.views.warehouse_product_history import (
    WarehouseProductHistoryListAPIView
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
    path('warehouseproduct/create/', WarehouseProductCreateAPIView.as_view()),
    path('warehouseproduct/list/', WarehouseProductListAPIView.as_view()),
    path('warehouseproduct/detailed/<int:pk>/', WarehouseProductRetrieveAPIView.as_view()),
    path('warehouseproduct/update/<int:pk>/', WarehouseProductRetrieveUpdateDestroyView.as_view()),
    path('warehouseproduct/create_by_barcode/', WarehouseProductCreateByBarcodeAPIView.as_view()),
    path('palleting/create/', PalletingCreateAPIView.as_view()),
    path('palleting/list/', PalletingListAPIView.as_view()),
    path('palleting/detailed/<int:pk>/', PalletingRetrieveAPIView.as_view()),
    path('palleting/update/<int:pk>/', PalletingRetrieveUpdateDestroyAPIView.as_view()),
    path('warehousettn/', WarehouseTTNListCreateAPIView.as_view()),
    path('warehousettnbyuser/', WarehouseTTNByUserIdAPIView.as_view()),
    path('warehousettn/update/<int:pk>/', WarehouseTTNRetrieveUpdateDestroyAPIView.as_view()),
    path('warehouseproducthistory/', WarehouseProductHistoryListAPIView.as_view()),
]
