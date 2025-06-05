from django.urls import path

from apps.invoice.views.invoice import (
    InvoiceCreateAPIView,
    InvoiceListAPIView,
    InvoiceRetrieveAPIView,
    InvoiceRetrieveUpdateDestroyAPIView,
)
from apps.invoice.views.invoice_container import (
    InvoiceContainerCreateAPIView,
    InvoiceContainerListAPIView,
    InvoiceContainerRetrieveAPIView,
    InvoiceContainerRetrieveUpdateDestroyAPIView,
)


urlpatterns = [
    path('invoice_file/create/', InvoiceCreateAPIView.as_view()),
    path('invoice_file/list/', InvoiceListAPIView.as_view()),
    path('invoice_file/detailed/<int:pk>/', InvoiceRetrieveAPIView.as_view()),
    path('invoice_file/update/<int:pk>/', InvoiceRetrieveUpdateDestroyAPIView.as_view()),
    path('invoice_container/create/', InvoiceContainerCreateAPIView.as_view()),
    path('invoice_container/list/', InvoiceContainerListAPIView.as_view()),
    path('invoice_container/detailed/<int:pk>/', InvoiceContainerRetrieveAPIView.as_view()),
    path('invoice_container/update/<int:pk>/', InvoiceContainerRetrieveUpdateDestroyAPIView.as_view()),
]
