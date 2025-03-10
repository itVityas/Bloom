from django.urls import path

from apps.arrival.views.clearance_invoice import (
    ClearanceInvoiceListCreateAPIView,
    ClearanceInvoiceDetailedView,
    GetFullClearanceInvoiceView,
    GetFullClearancesInvoiceListView)
from apps.arrival.views.clearance_invoice_items import ClearanceInvoiceItemDetailedView, \
    ClearanceInvoiceItemListCreateAPIView
from apps.arrival.views.cleared_item import ClearedItemDetailedView, ClearedItemListCreateAPIView
from apps.arrival.views.declaration import (
    DeclarationListCreateAPIView, DeclarationDetailedView,
    DeclarationAndItemView, DeclarationAndItemDetailedView,
    DeclarationAndItemCreateAPIView, BindDeclarationsToContainerAPIView
)
from apps.arrival.views.declared_item import (
    DeclaredItemListCreateAPIView, DeclaredItemDetailedView
)
from apps.arrival.views.order import (
    OrderCreateAPIView, OrderListView, OrderDetailedView,
    OrderAndContainerListView, OrderAndContainerDetailView
)
from apps.arrival.views.content import ContentListView, ContentDetailView
from apps.arrival.views.container import (
    ContainerListView, ContainerCreateView, ContainerUpdateView,
    ContainerAndDeclarationView, ContainerAndDeclarationDetailView, BindContainersToOrderAPIView
)

urlpatterns = [
    # Order endpoints
    path('order/', OrderListView.as_view(), name='order-list'),
    path('order/create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('order/detailed/<int:pk>/', OrderDetailedView.as_view(), name='order-detail'),
    path('order_and_container/', OrderAndContainerListView.as_view(), name='order-and-container-list'),
    path('order_and_container/<int:pk>/', OrderAndContainerDetailView.as_view(), name='order-and-container-detail'),

    # Container endpoints
    path('container/', ContainerListView.as_view(), name='container-list'),
    path('container/create/', ContainerCreateView.as_view(), name='container-create'),
    path('container/detailed/<int:pk>/', ContainerUpdateView.as_view(), name='container-update'),
    path('container_and_declaration/', ContainerAndDeclarationView.as_view(), name='container-and-declaration-list'),
    path('container_and_declaration/<int:pk>/', ContainerAndDeclarationDetailView.as_view(),
         name='container-and-declaration-detail'),
    path('container/assign/', BindContainersToOrderAPIView.as_view(), name='bind-containers'),

    # Declaration endpoints
    path('declaration/', DeclarationListCreateAPIView.as_view(), name='declaration-list'),
    path('declaration/detailed/<int:pk>/', DeclarationDetailedView.as_view(), name='declaration-detail'),
    path('declaration_and_items/', DeclarationAndItemView.as_view(), name='declaration-and-item-list'),
    path('declaration_and_items/<int:pk>/', DeclarationAndItemDetailedView.as_view(),
         name='declaration-and-item-detail'),
    path('declaration_and_items/create/', DeclarationAndItemCreateAPIView.as_view(),
         name='declaration-and-item-create'),
    path('declaration/assign/', BindDeclarationsToContainerAPIView.as_view(), name='bind-declarations'),

    # DeclaredItem endpoints
    path('declared_item/', DeclaredItemListCreateAPIView.as_view(), name='declared-item-list'),
    path('declared_item/detailed/<int:pk>/', DeclaredItemDetailedView.as_view(), name='declared-item-detail'),

    # Content endpoints
    path('content/', ContentListView.as_view(), name='content-list'),
    path('content/detailed/<int:pk>/', ContentDetailView.as_view(), name='content-detail'),

    # ClearanceInvoice endpoints
    path('clearance_invoice/', ClearanceInvoiceListCreateAPIView.as_view(), name='clearance-invoice-list'),
    path('clearance_invoice/detailed/<int:pk>/', ClearanceInvoiceDetailedView.as_view(),
         name='clearance-invoice-detail'),
    path('clearance_invoice/full/<int:pk>/', GetFullClearanceInvoiceView.as_view()),
    path('clearance_invoice/full/', GetFullClearancesInvoiceListView.as_view()),

    # ClearanceInvoiceItems endpoints
    path('clearance_invoice_items/', ClearanceInvoiceItemListCreateAPIView.as_view(),
         name='clearance-invoice-item-list'),
    path('clearance_invoice_items/detailed/<int:pk>/', ClearanceInvoiceItemDetailedView.as_view(),
         name='clearance-invoice-item-detail'),

    # ClearedItem endpoints
    path('cleared_item/', ClearedItemListCreateAPIView.as_view(), name='cleared-item-list'),
    path('cleared_item/detailed/<int:pk>/', ClearedItemDetailedView.as_view(), name='cleared-item-detail'),
]
