from django.urls import path

from apps.sez.views.report_stz1 import ReportSTZ1View

urlpatterns = [
    path('reportstz1/', ReportSTZ1View.as_view()),
]
