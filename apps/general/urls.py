from django.urls import path

from apps.general.views.visits import (
    VisitsListCreateView, VisitsRetrieveUpdateDestroyView
)

urlpatterns = [
    path('visits/', VisitsListCreateView.as_view()),
    path('visits/detailed/<int:pk>/', VisitsRetrieveUpdateDestroyView.as_view()),
]
