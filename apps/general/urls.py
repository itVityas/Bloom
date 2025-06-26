from django.urls import path

from apps.general.views.logs import LogDjangoDownloadView, LogOmegaDownloadView
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
    path('add-title/detailed/<int:pk>/', AddTitleRetrieveUpdateDestroyAPIView.as_view()),

    # Logs
    path('logs/django_download/', LogDjangoDownloadView.as_view(), name='django-log-download'),
    path('logs/omega_download/', LogOmegaDownloadView.as_view(), name='omega-log-download'),

]
