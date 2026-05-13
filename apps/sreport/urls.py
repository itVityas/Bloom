from django.urls import path

from apps.sreport.views.module_numbers import ModuleNumbersView
from apps.sreport.views.relevant_models_number import RelevantModelNumberView
from apps.sreport.views.data_for_main_doc import DataForMainDocView
from apps.sreport.views.report_storage import ReportStorageView
from apps.sreport.views.name_count import ModelNameCountView
from apps.sreport.views.product_plan import ProductPlanCreateView, ProductPlanListView, ProductPlanUpdateView
from apps.sreport.views.onec_ttn_item_scaned_count import (
    OneCTTNItemScanedCountAPIView,
    OneCTTNItemScanedCountFullAPIView
)
from apps.sreport.views.warehouse_ttn_barcode import WarehouseTTNBarcodeListAPIView


urlpatterns = [
    path('report/module-number/', ModuleNumbersView.as_view(), name='module-number'),
    path('report/relevant-model-number/', RelevantModelNumberView.as_view(), name='relevant-model-number'),
    path('report/data-for-main-doc/', DataForMainDocView.as_view(), name='data-for-main-doc'),
    path('warehouse/report_storage/', ReportStorageView.as_view()),
    path('warehouse/name_count/', ModelNameCountView.as_view()),
    path('product_plan/create/', ProductPlanCreateView.as_view()),
    path('product_plan/list/', ProductPlanListView.as_view()),
    path('product_plan/update/<int:pk>/', ProductPlanUpdateView.as_view()),
    path('warehouse/1c_ttn_item_scanned_count_view/', OneCTTNItemScanedCountAPIView.as_view()),
    path('warehouse/1c_ttn_item_scanned_count_full/', OneCTTNItemScanedCountFullAPIView.as_view()),
    path('warehouse/warehouse_ttn_barcode/', WarehouseTTNBarcodeListAPIView.as_view()),
]
