from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view

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
    queryset = SiteLock.objects.all()


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
    queryset = SiteLock.objects.all()
