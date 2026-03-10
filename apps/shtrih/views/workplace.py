from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.shtrih.models import Workplaces
from apps.shtrih.serializers.workplaces import WorkplacesSerializer


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='List workplaces',
        description="description='Permission: admin, strih"
    )
)
class WorkplaceListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WorkplacesSerializer
    queryset = Workplaces.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
