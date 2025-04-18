from django.urls import path

from apps.shtrih.views.color import ColorsListView
from apps.shtrih.views.module import ModulesListView
from apps.shtrih.views.production_code import ProductionCodeListView
from apps.shtrih.views.model_name import ModelNameListView
from apps.shtrih.views.model import ModelListView

urlpatterns = [
    path('strih/colors', ColorsListView.as_view()),
    path('strih/modules', ModulesListView.as_view()),
    path('strih/production_code', ProductionCodeListView.as_view()),
    path('strih/model_name', ModelNameListView.as_view()),
    path('strih/models', ModelListView.as_view()),
]
