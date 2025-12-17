from django.urls import path

from apps.omega.views.compound import CompoundOfModelWithAnalogs


urlpatterns = [
    path('omega/compound/', CompoundOfModelWithAnalogs.as_view(), name='compound-of-model-with-analogs')
]
