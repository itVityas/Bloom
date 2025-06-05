from django.urls import path

from apps.invoice.views.invoice import (
    InvoiceCreateAPIView,
    InvoiceListAPIView,
    InvoiceRetrieveAPIView,
    InvoiceRetrieveUpdateDestroyAPIView
)


urlpatterns = [
    path('invoice/create/', InvoiceCreateAPIView.as_view()),
    path('invoice/list/', InvoiceListAPIView.as_view()),
    path('invoice/detailed/<int:pk>/', InvoiceRetrieveAPIView.as_view()),
    path('invoice/update/<int:pk>/', InvoiceRetrieveUpdateDestroyAPIView.as_view()),
]
