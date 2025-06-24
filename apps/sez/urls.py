from django.urls import path

from apps.sez.views.clearance_workflow.clearance_result import ClearanceResultListAPIView
from apps.sez.views.clearance_workflow.cleared_item_by_clearance import ClearedItemListAPIView
from apps.sez.views.clearance_workflow.export_products import ClearanceInvoiceProductsExportView
from apps.sez.views.clearance_workflow.full_clearance_workflow import FullClearanceWorkflowAPIView
from apps.sez.views.create_dbf import ClearanceInvoiceDBFZipView
from apps.sez.views.report_stz1 import ReportSTZ1View
from apps.sez.views.report_clearanceinvoice import ReportClearanceInvoicePDFView
from apps.sez.views.clearance_invoice import (
    ClearanceInvoiceDetailedView,
    ClearanceInvoiceListCreateAPIView,
    GetFullClearanceInvoiceView,
    GetFullClearancesInvoiceListView,
)
from apps.sez.views.clearance_invoice_items import (
    ClearanceInvoiceItemDetailedView,
    ClearanceInvoiceItemListCreateAPIView,
)
from apps.sez.views.cleared_item import (
    ClearedItemDetailedView,
    ClearedItemListCreateAPIView,
)
from apps.sez.views.document_sez import DocumentSezView, CustomClearanceView
from apps.sez.views.barcode_table import BarcodeTable
from apps.sez.views.report_delete import ReportDeleteView
from apps.sez.views.available_declarations import GetAvailableDeclarationsView
from apps.sez.views.name_amount import NameAmountView
from apps.sez.views.inner_ttn import (
    InnerTTNListView,
    InnerTTNCreateView,
    InnerTTNPDFView,
    InnerTTNDetailedView,
    InnerTTNStandardUpdateView,
    InnerTTNDetailedByUUIDView,
)
from apps.sez.views.inner_ttn_items import (
    InnerTTNItemsListView,
    InnerTTNItemsCreateView,
    InnerTTNItemsRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    # Reports
    path('reportstz1/', ReportSTZ1View.as_view()),
    path('reportclearancepdf/', ReportClearanceInvoicePDFView.as_view()),

    # ClearanceInvoice endpoints
    path('clearance_invoice/', ClearanceInvoiceListCreateAPIView.as_view(), name='clearance-invoice-list'),
    path('clearance_invoice/detailed/<int:pk>/', ClearanceInvoiceDetailedView.as_view(),
         name='clearance-invoice-detail'),
    path('clearance_invoice/full/<int:pk>/', GetFullClearanceInvoiceView.as_view()),
    path('clearance_invoice/full/', GetFullClearancesInvoiceListView.as_view()),
    path('clearance_invoice/reportdelete/<int:pk>/', ReportDeleteView.as_view()),

    # ClearanceInvoiceItems endpoints
    path('clearance_invoice_items/', ClearanceInvoiceItemListCreateAPIView.as_view(),
         name='clearance-invoice-item-list'),
    path('clearance_invoice_items/detailed/<int:pk>/', ClearanceInvoiceItemDetailedView.as_view(),
         name='clearance-invoice-item-detail'),

    # ClearedItem endpoints
    path('cleared_item/', ClearedItemListCreateAPIView.as_view(), name='cleared-item-list'),
    path('cleared_item/detailed/<int:pk>/', ClearedItemDetailedView.as_view(), name='cleared-item-detail'),

    # sez
    path('available_declarations/', GetAvailableDeclarationsView.as_view()),
    path('name-amount/', NameAmountView.as_view()),

    # Document SEZ
    path('document_sez/', DocumentSezView.as_view()),
    path('custom_clearance/', CustomClearanceView.as_view()),
    path('barcode_table/', BarcodeTable.as_view()),

    # InnerTTN
    path('innerttn/', InnerTTNListView.as_view()),
    path('innerttn/create/', InnerTTNCreateView.as_view()),
    path('innerttn/pdf/<int:pk>/', InnerTTNPDFView.as_view()),
    path('innerttn/detailed/<int:pk>/', InnerTTNDetailedView.as_view()),
    path('innerttn/uuid/<str:uuid>/', InnerTTNDetailedByUUIDView.as_view()),
    path('innerttn/standard_update/<int:pk>/', InnerTTNStandardUpdateView.as_view()),
    path('innerttn_items/', InnerTTNItemsListView.as_view()),
    path('innerttn_items/create/', InnerTTNItemsCreateView.as_view()),
    path('innerttn_items/<int:pk>/', InnerTTNItemsRetrieveUpdateDestroyAPIView.as_view()),

    # Full clearance_workflow
    path('clearance/calculate/', FullClearanceWorkflowAPIView.as_view(), name='full-clearance-workflow'),
    path('clearance/<int:invoice_id>/cleared-items/', ClearedItemListAPIView.as_view(),
         name='cleared-item-list'),
    path('clearance/<int:invoice_id>/cleared-result/', ClearanceResultListAPIView.as_view(),
         name='cleared-result-list'),
    path('clearance/<int:invoice_id>/products/', ClearanceInvoiceProductsExportView.as_view(),
         name='products-export'),
    path('clearance-invoices/<int:clearance_invoice_id>/dbf-zip/', ClearanceInvoiceDBFZipView.as_view(),
         name='clearance-invoice-dbf-zip'),

]
