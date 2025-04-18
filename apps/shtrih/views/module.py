from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.shtrih.models import Modules
from apps.shtrih.serializers.module import ModulesSerializer
from apps.shtrih.permission import StrihPermission
from Bloom.paginator import StandartResultPaginator


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='List modules',
        description="description='Permission: admin, strih"
    )
)
class ModulesListView(ListAPIView):
    permission_classes = (IsAuthenticated, StrihPermission)
    serializer_class = ModulesSerializer
    queryset = Modules.objects.all()
    pagination_class = StandartResultPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'digit', 'digit']
