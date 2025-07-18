"""
URL configuration for Bloom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # DJANGO-ADMIN
    path('admin/', admin.site.urls),
    # swagger
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path("api/v1/schema/redoc/", SpectacularRedocView.as_view(
        url_name="schema")),

    # autorization
    path('api/v1/token/refresh/', TokenRefreshView.as_view()),
    path('api/v1/token/verify/', TokenVerifyView.as_view()),

    path('api/v1/', include('apps.account.urls')),
    path('api/v1/', include('apps.arrival.urls')),
    path('api/v1/', include('apps.declaration.urls')),
    path('api/v1/', include('apps.sgp.urls')),
    path('api/v1/', include('apps.invoice.urls')),
    path('api/v1/', include('apps.sez.urls')),
    path('api/v1/', include('apps.omega.urls')),
    path('api/v1/', include('apps.shtrih.urls')),
    path('api/v1/', include('apps.general.urls')),
    path('api/v1/', include('apps.onec.urls')),
    path('api/v1/', include('apps.warehouse.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
