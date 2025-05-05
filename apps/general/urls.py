from django.urls import path

from apps.general.views.visits import (
    VisitsListCreateView, VisitsRetrieveUpdateDestroyView
)
from apps.general.views.add_body import (
    AddBodyListCreateAPIView, AddBodyRetrieveUpdateDestroyAPIView
)
from apps.general.views.add_title import (
    AddTitleCreateAPIView,
    AddTitleListAPIView,
    AddTitleRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('visits/', VisitsListCreateView.as_view()),
    path('visits/detailed/<int:pk>/', VisitsRetrieveUpdateDestroyView.as_view()),
    path('add-body/', AddBodyListCreateAPIView.as_view()),
    path('add-body/detailed/<int:pk>/', AddBodyRetrieveUpdateDestroyAPIView.as_view()),
    path('add-title/', AddTitleListAPIView.as_view()),
    path('add-title/create/', AddTitleCreateAPIView.as_view()),
    path('add-title/detailed/<int:pk>/', AddTitleRetrieveUpdateDestroyAPIView.as_view())
]
