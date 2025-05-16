from django.urls import path

from apps.declaration.views.declaration import (
    DeclarationListCreateAPIView, DeclarationDetailedView,
    DeclarationAndItemView, DeclarationAndItemDetailedView,
    DeclarationAndItemCreateAPIView, BindDeclarationsToContainerAPIView, DeclarationBulkDeleteAPIView
)
from apps.declaration.views.declared_item import (
    DeclaredItemListCreateAPIView, DeclaredItemDetailedView
)
from apps.declaration.views.upload_declaration import ZipFileUploadAPIView

urlpatterns = [
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
    path('declaration/upload_zip/', ZipFileUploadAPIView.as_view(), name='zip-upload'),
    path('declaration/delete_all_declaration/', DeclarationBulkDeleteAPIView.as_view(), name='delete-all'),
]