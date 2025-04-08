from django.urls import path

from apps.omega.views.vz_norm import VzNormListAPIView

urlpatterns = [
    path('omega/', VzNormListAPIView.as_view(), name='vznorms-list'),
]
