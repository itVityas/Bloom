from django.urls import path

from apps.omega.views.vz_nab import VzNabListAPIView
from apps.omega.views.vz_norm import VzNormListAPIView


urlpatterns = [
    path('omega/vz_norm/', VzNormListAPIView.as_view(), name='vznorms-list'),
    path('omega/vz_nab/', VzNabListAPIView.as_view(), name='vznab-list'),

]
