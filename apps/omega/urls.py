from django.urls import path

from apps.omega.views.vz_nab import VzNabListAPIView
from apps.omega.views.vz_norm import VzNormListAPIView
from apps.omega.views.clear_items import ClearItemsView


urlpatterns = [
    path('omega/vz_norm/', VzNormListAPIView.as_view(), name='vznorms-list'),
    path('omega/vz_nab/', VzNabListAPIView.as_view(), name='vznab-list'),
    path("omega/clear_items/", ClearItemsView.as_view(), name="clear-items"),

]
