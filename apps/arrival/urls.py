from django.urls import path

from apps.arrival.views.declaration import (
    DeclarationListCreateAPIView, DeclarationDetailedView,
    DeclarationAndItemView, DeclarationAndItemDetailedView,
    DeclarationAndItemCreateAPIView)
from apps.arrival.views.declared_item import (
    DeclaredItemListCreateAPIView, DeclaredItemDetailedView)
from apps.arrival.views.order import (
    OrderCreateAPIView, OrderListView, OrderDetailedView, OrderAndContainerListView, OrderAndContainerDetailView)
from apps.arrival.views.content import ContentListView, ContentDetailView
from apps.arrival.views.conteiner import (
    ContainerListView, ContainerCreateView, ContainerUpdateView, ContainerAndDeclarationView,
    ContainerAndDeclarationDetailView)

urlpatterns = [
    # order
    path('order/', OrderListView.as_view()),
    path('order/create/', OrderCreateAPIView.as_view()),
    path('order/detailed/<int:pk>/', OrderDetailedView.as_view()),
    path('order_and_container/', OrderAndContainerListView.as_view()),
    path('order_and_container/<int:pk>/', OrderAndContainerDetailView.as_view()),

    # declaration
    path('declaration/', DeclarationListCreateAPIView.as_view()),
    path('declaration/detailed/<int:pk>/', DeclarationDetailedView.as_view()),
    path('declaration_and_items/', DeclarationAndItemView.as_view()),
    path('declaration_and_items/<int:pk>/', DeclarationAndItemDetailedView.as_view()),
    path('declaration_and_items/create/', DeclarationAndItemCreateAPIView.as_view()),

    # DeclaredItem
    path('declared_item/', DeclaredItemListCreateAPIView.as_view()),
    path('declared_item/detailed/<int:pk>/', DeclaredItemDetailedView.as_view()),

    # Content
    path('content/', ContentListView.as_view()),
    path('content/detailed/<int:pk>/', ContentDetailView.as_view()),

    # Container
    path('container/', ContainerListView.as_view()),
    path('container/create/', ContainerCreateView.as_view()),
    path('container/detailed/<int:pk>/', ContainerUpdateView.as_view()),
    path('container_and_declaration/', ContainerAndDeclarationView.as_view()),
    path('container_and_declaration/<int:pk>/', ContainerAndDeclarationDetailView.as_view()),
]
