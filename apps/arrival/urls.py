from django.urls import path

from apps.arrival.views.order import OrderListCreateAPIView, OrderDetailedView
from apps.arrival.views.content import ContentListView, ContentDetailView
from apps.arrival.views.conteiner import (
    ContainerListView, ContainerCreateView, ContainerUpdateView)

urlpatterns = [
    # order
    path('order/', OrderListCreateAPIView.as_view()),
    path('order/detailed/<int:pk>/', OrderDetailedView.as_view()),
    # Content
    path('content/', ContentListView.as_view()),
    path('content/detailed/<int:pk>/', ContentDetailView.as_view()),
    # Container
    path('container/', ContainerListView.as_view()),
    path('container/create/', ContainerCreateView.as_view()),
    path('container/detailed/<int:pk>/', ContainerUpdateView.as_view()),
]
