from django.urls import path

from apps.sgp.views.consignment import ConsignmentCreateView


urlpatterns = [
    path('consignment/', ConsignmentCreateView.as_view()),
]
