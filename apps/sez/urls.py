from django.urls import path

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
from apps.sez.views.document_sez import DocumentSezView
from apps.sez.views.available_declarations import GetAvailableDeclarationsView

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

    # Document SEZ
    path('document_sez/', DocumentSezView.as_view()),
]
