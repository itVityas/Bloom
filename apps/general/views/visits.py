from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.general.models import Visits
from apps.general.serializers.visits import VisitsSerializers


@extend_schema(tags=['Visits'])
@extend_schema_view(
    get=extend_schema(
        summary='Get list of visits',
        description='Permission: authorized',
    ),
    post=extend_schema(
        summary='Create visits',
        description='Permission: authorized',
    )
)
class VisitsListCreateView(ListCreateAPIView):
    """
    API endpoint for listing and creating user visit records.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Visits.objects.all()
    serializer_class = VisitsSerializers
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['user',]


@extend_schema(tags=['Visits'])
@extend_schema_view(
    get=extend_schema(
        summary='Get visits',
        description='Permission: authorized',
    ),
    put=extend_schema(
        summary='Update visits',
        description='Permission: authorized',
    ),
    patch=extend_schema(
        summary='Update visits',
        description='Permission: authorized',
    ),
    delete=extend_schema(
        summary='Delete visits',
        description='Permission: authorized',
    )
)
class VisitsRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating and deleting visit records.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Visits.objects.all()
    serializer_class = VisitsSerializers
