from django.urls import path

from apps.onec.views.weight import Weight1cView

urlpatterns = [
    path('1c/weight/', Weight1cView.as_view()),
]
