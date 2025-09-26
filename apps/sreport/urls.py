from django.urls import path

from apps.sreport.views.module_numbers import ModuleNumbersView
from apps.sreport.views.relevant_models_number import RelevantModelNumberView


urlpatterns = [
    path('report/module-number/', ModuleNumbersView.as_view(), name='module-number'),
    path('report/relevant-model-number/', RelevantModelNumberView.as_view(), name='relevant-model-number'),
]
