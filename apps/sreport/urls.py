from django.urls import path

from apps.sreport.views.module_numbers import ModuleNumbersView
from apps.sreport.views.relevant_models_number import RelevantModelNumberView
from apps.sreport.views.data_for_main_doc import DataForMainDocView


urlpatterns = [
    path('report/module-number/', ModuleNumbersView.as_view(), name='module-number'),
    path('report/relevant-model-number/', RelevantModelNumberView.as_view(), name='relevant-model-number'),
    path('report/data-for-main-doc/', DataForMainDocView.as_view(), name='data-for-main-doc'),
]
