from django.urls import path

from apps.arrival.views.declaration import (
    DeclarationListCreateAPIView, DeclarationDetailedView, DeclarationAndItemView, DeclarationAndItemDetailedView)
from apps.arrival.views.declared_item import DeclaredItemListCreateAPIView, DeclaredItemDetailedView
from apps.arrival.views.order import OrderListCreateAPIView, OrderDetailedView
from apps.arrival.views.content import ContentListView, ContentDetailView
from apps.arrival.views.conteiner import (
    ContainerListView, ContainerCreateView, ContainerUpdateView)

urlpatterns = [
    # order
    path('order/', OrderListCreateAPIView.as_view()),
    path('order/detailed/<int:pk>/', OrderDetailedView.as_view()),

    # declaration
    path('declaration/', DeclarationListCreateAPIView.as_view()),
    path('declaration/detailed/<int:pk>/', DeclarationDetailedView.as_view()),
    path('declaration_and_items/', DeclarationAndItemView.as_view()),
    path('declaration_and_items/<int:pk>/', DeclarationAndItemDetailedView.as_view()),

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
]
