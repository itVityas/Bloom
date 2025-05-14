from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view


from apps.sez.models import InnerTTN
from apps.sez.serializers.inner_ttn import InnerTTNSerializer
from apps.sez.permissions import STZPermission


@extend_schema(tags=['InnerTTN'])
@extend_schema_view(
    get=extend_schema(
        summary='get list Inner TTN',
        description='Permission: admin, stz_reader, stz'
    )
)
class InnerTTNListView(ListAPIView):
    permission_classes = (IsAuthenticated, STZPermission)
    serializer_class = InnerTTNSerializer
    queryset = InnerTTN.objects.all()
