from django.urls import path

from apps.invoice.views.traindoc import (
    TrainDocCreateAPIView,
    TrainDocListAPIView,
    TrainDocRetrieveAPIView,
    TrainDocRetrieveUpdateDestroyAPIView,
)
from apps.invoice.views.invoice_container import (
    InvoiceContainerCreateAPIView,
    InvoiceContainerListAPIView,
    InvoiceContainerRetrieveAPIView,
    InvoiceContainerRetrieveUpdateDestroyAPIView,
)
from apps.invoice.views.sheet_to_excel import InvoiceContainerSheetView


urlpatterns = [
    path('traindoc/create/', TrainDocCreateAPIView.as_view()),
    path('traindoc/list/', TrainDocListAPIView.as_view()),
    path('traindoc/detailed/<int:pk>/', TrainDocRetrieveAPIView.as_view()),
    path('traindoc/update/<int:pk>/', TrainDocRetrieveUpdateDestroyAPIView.as_view()),
    path('invoice_container/create/', InvoiceContainerCreateAPIView.as_view()),
    path('invoice_container/list/', InvoiceContainerListAPIView.as_view()),
    path('invoice_container/detailed/<int:pk>/', InvoiceContainerRetrieveAPIView.as_view()),
    path('invoice_container/update/<int:pk>/', InvoiceContainerRetrieveUpdateDestroyAPIView.as_view()),
    path('invoice_container/sheet/', InvoiceContainerSheetView.as_view()),
]
