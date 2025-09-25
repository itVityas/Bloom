from django.urls import path

from apps.sreport.views.module_numbers import ModuleNumbersView


urlpatterns = [
    path('report/module-number/', ModuleNumbersView.as_view(), name='module-number'),
]
