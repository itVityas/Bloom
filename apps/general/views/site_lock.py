from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.core.cache import cache
from rest_framework.response import Response

from apps.general.models import SiteLock
from apps.general.serializers.site_lock import SiteLockSerializer


@extend_schema(tags=['Site lock'])
@extend_schema_view(
    get=extend_schema(
        summary='Get site lock',
        description='AllowAny',
        responses={200: SiteLockSerializer},
    ),
    post=extend_schema(
        summary='Create site lock',
        description='AllowAny',
        responses={200: SiteLockSerializer},
    ),
)
class SiteLockView(ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SiteLockSerializer

    CACHE_KEY = 'singleton_site_lock'
    CACHE_TIMEOUT = 60 * 5

    def get_queryset(self):
        """Для GET запросов используем кэшированный singleton"""
        if self.request.method == 'GET':
            cached_instance = cache.get(self.CACHE_KEY)

            if cached_instance is not None:
                return SiteLock.objects.filter(pk=cached_instance.pk)

            instance = SiteLock.objects.first()
            if instance:
                cache.set(self.CACHE_KEY, instance, self.CACHE_TIMEOUT)
                return SiteLock.objects.filter(pk=instance.pk)

        return SiteLock.objects.all()

    def list(self, request, *args, **kwargs):
        """Переопределяем list для работы с singleton"""
        queryset = self.filter_queryset(self.get_queryset())

        if queryset.exists():
            serializer = self.get_serializer(queryset.first())
            return Response(serializer.data)

        return Response({})

    def create(self, request, *args, **kwargs):
        """При создании/обновлении инвалидируем кэш"""
        response = super().create(request, *args, **kwargs)
        cache.delete(self.CACHE_KEY)
        return response


@extend_schema(tags=['Site lock'])
@extend_schema_view(
    get=extend_schema(
        summary='Get site lock',
        description='AllowAny',
        responses={200: SiteLockSerializer},
    ),
    put=extend_schema(
        summary='Update site lock',
        description='AllowAny',
        responses={200: SiteLockSerializer},
    ),
    patch=extend_schema(
        summary='Update site lock',
        description='AllowAny',
        responses={200: SiteLockSerializer},
    ),
)
class SiteLockUpdateView(RetrieveUpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SiteLockSerializer

    CACHE_KEY = 'singleton_site_lock'
    CACHE_TIMEOUT = 60 * 5

    def get_queryset(self):
        """Для GET запросов используем кэшированный singleton"""
        if self.request.method == 'GET':
            cached_instance = cache.get(self.CACHE_KEY)

            if cached_instance is not None:
                return SiteLock.objects.filter(pk=cached_instance.pk)

            instance = SiteLock.objects.first()
            if instance:
                cache.set(self.CACHE_KEY, instance, self.CACHE_TIMEOUT)
                return SiteLock.objects.filter(pk=instance.pk)

        return SiteLock.objects.all()
