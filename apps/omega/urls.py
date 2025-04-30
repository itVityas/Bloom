from django.urls import path

from apps.omega.views.clear_items import ClearItemsView


urlpatterns = [
    path("omega/clear_items/", ClearItemsView.as_view(), name="clear-items"),

]
