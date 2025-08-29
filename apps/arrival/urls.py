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
    ContainerAndContentCreateView,
    ContainerListUpdateView
)
from apps.arrival.views.report import ReportCSVView
from apps.arrival.views.lot import (
    LotCreateAPIView,
    LotListAPIView,
    LotRetrieveUpdateDestroyAPIView,
)
from apps.arrival.views.lot_model import (
    LotModelListCreateAPIView,
    LotModelRetrieveUpdateDestroyAPIView,
)
from apps.arrival.views.makeup import (
    MakeUpCreateView,
    MakeUpListView,
    MakeUpRetrieveUpdateDestroyView,
)

urlpatterns = [
    # Order endpoints
    path('order/', OrderListView.as_view(), name='order-list'),
    path('order/create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('order/detailed/<int:pk>/', OrderDetailedView.as_view(), name='order-detail'),
    path('order_and_container/', OrderAndContainerListView.as_view(), name='order-and-container-list'),
    path('order_and_container/<int:pk>/', OrderAndContainerDetailView.as_view(), name='order-and-container-detail'),
    path('order/report/', ReportCSVView.as_view()),

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
    path('container/listupdate/', ContainerListUpdateView.as_view()),

    # Content endpoints
    path('content/', ContentListView.as_view()),
    path('content/detailed/<int:pk>/', ContentDetailView.as_view()),

    # Lot endpoints
    path('lot/create/', LotCreateAPIView.as_view()),
    path('lot/list/', LotListAPIView.as_view()),
    path('lot/update/<int:pk>/', LotRetrieveUpdateDestroyAPIView.as_view()),

    # Lot Model
    path('lot_model/', LotModelListCreateAPIView.as_view()),
    path('lot_model/detail/<int:pk>/', LotModelRetrieveUpdateDestroyAPIView.as_view()),

    # MakeUp endpoints
    path('makeup/create/', MakeUpCreateView.as_view()),
    path('makeup/list/', MakeUpListView.as_view()),
    path('makeup/detail/<int:pk>/', MakeUpRetrieveUpdateDestroyView.as_view()),
]
