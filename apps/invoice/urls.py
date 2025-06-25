from django.urls import path

from apps.invoice.views.traindoc import (
    TrainDocCreateAPIView,
    TrainDocListAPIView,
    TrainDocRetrieveAPIView,
    TrainDocRetrieveUpdateDestroyAPIView,
    TrainDocByLotAPIView,
)
from apps.invoice.views.invoice_container import (
    InvoiceContainerCreateAPIView,
    InvoiceContainerListAPIView,
    InvoiceContainerRetrieveAPIView,
    InvoiceContainerRetrieveUpdateDestroyAPIView,
)
from apps.invoice.views.sheet_to_excel import (
    InvoiceContainerSheetView, InvoiceByContainerNumberAPIView)
from apps.invoice.views.invoice_to_html import InvoiceToPDFView


urlpatterns = [
    path('traindoc/create/', TrainDocCreateAPIView.as_view()),
    path('traindoc/list/', TrainDocListAPIView.as_view()),
    path('traindoc/detailed/<int:pk>/', TrainDocRetrieveAPIView.as_view()),
    path('traindoc/update/<int:pk>/', TrainDocRetrieveUpdateDestroyAPIView.as_view()),
    path('traindoc/by_lot/<int:pk>/', TrainDocByLotAPIView.as_view()),
    path('invoice_container/create/', InvoiceContainerCreateAPIView.as_view()),
    path('invoice_container/list/', InvoiceContainerListAPIView.as_view()),
    path('invoice_container/detailed/<int:pk>/', InvoiceContainerRetrieveAPIView.as_view()),
    path('invoice_container/update/<int:pk>/', InvoiceContainerRetrieveUpdateDestroyAPIView.as_view()),
    path('invoice_container/sheet/', InvoiceContainerSheetView.as_view()),
    path('invoice/by_container_number/', InvoiceByContainerNumberAPIView.as_view()),
    path('invoice/to_html/', InvoiceToPDFView.as_view()),
]
