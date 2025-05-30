from django.urls import path

from apps.invoice.views.invoice_item import (
    InvoiceItemListCreateView, InvoiceItemDetailedView)
from apps.invoice.views.invoice import (
    InvoiceCreateAPIView, InvoiceDetailedAPIView, InvoiceListAPIView
)
from apps.invoice.views.report_invoice import ReportPDFInvoice
from apps.invoice.views.report_invoice_exel import ReportXLSXInvoice

urlpatterns = [
    # InvoiceItem
    path('invoiceitem/', InvoiceItemListCreateView.as_view()),
    path('invoiceitem/detailed/<int:pk>/', InvoiceItemDetailedView.as_view()),
    # Invoice
    path('invoice/', InvoiceListAPIView.as_view()),
    path('invoice/create/', InvoiceCreateAPIView.as_view()),
    path('invoice/detailed/<int:pk>/', InvoiceDetailedAPIView.as_view()),
    path('invoice/report/', ReportPDFInvoice.as_view()),
    path('invoice/report/exel/', ReportXLSXInvoice.as_view()),
]
