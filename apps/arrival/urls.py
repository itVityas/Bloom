from django.urls import path

from apps.arrival.views.order import (
    OrderCreateAPIView, OrderListView, OrderDetailedView,
    OrderAndContainerListView, OrderAndContainerDetailView
)
from apps.arrival.views.content import ContentListView, ContentDetailView
from apps.arrival.views.container import (
    ContainerListView,
    ContainerDetailView,
    ContainerCreateView,
    ContainerUpdateView,
    ContainerAndDeclarationView,
    ContainerAndDeclarationDetailView,
    BindContainersToOrderAPIView,
    ContainerAndContentCreateView
)

urlpatterns = [
    # Order endpoints
    path('order/', OrderListView.as_view(), name='order-list'),
    path('order/create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('order/detailed/<int:pk>/', OrderDetailedView.as_view(), name='order-detail'),
    path('order_and_container/', OrderAndContainerListView.as_view(), name='order-and-container-list'),
    path('order_and_container/<int:pk>/', OrderAndContainerDetailView.as_view(), name='order-and-container-detail'),

    # Container endpoints
    path('container/', ContainerListView.as_view()),
    path('container/create/', ContainerCreateView.as_view()),
    path('container/<int:pk>/', ContainerDetailView.as_view()),
    path('container/detailed/<int:pk>/', ContainerUpdateView.as_view()),
    path('container_and_declaration/', ContainerAndDeclarationView.as_view()),
    path('container_and_declaration/<int:pk>/', ContainerAndDeclarationDetailView.as_view(),
         name='container-and-declaration-detail'),
    path('container/assign/', BindContainersToOrderAPIView.as_view()),
    path('container_and_content/create/', ContainerAndContentCreateView.as_view()),

    # Content endpoints
    path('content/', ContentListView.as_view()),
    path('content/detailed/<int:pk>/', ContentDetailView.as_view()),
]
