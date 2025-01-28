from django.urls import path

from apps.arrival.views.order import OrderListCreateAPIView, OrderDetailedView

urlpatterns = [
    path('order/', OrderListCreateAPIView.as_view()),
    path('order/detailed/<int:pk>/', OrderDetailedView.as_view()),
]
