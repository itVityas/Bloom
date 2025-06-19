from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.arrival.models import MakeUp
from apps.arrival.serializers.makeup import (
    MakeUpGetSerializer, MakeUpPostSerializer)
from apps.arrival.permissions import ArrivalPermission


@extend_schema(tags=['MakeUp'])
@extend_schema_view(
    get=extend_schema(
        summary='List all makeups',
        description='List all makeups',
    ),
)
class MakeUpListView(ListAPIView):
    """
    List all makeups or create a new makeup.
    """
    queryset = MakeUp.objects.all()
    serializer_class = MakeUpGetSerializer
    permission_classes = [IsAuthenticated, ArrivalPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'lot']


@extend_schema(tags=['MakeUp'])
@extend_schema_view(
    post=extend_schema(
        summary='Create a new makeup',
        description='Create a new makeup',
    ),
)
class MakeUpCreateView(CreateAPIView):
    """
    Create a new makeup.
    """
    queryset = MakeUp.objects.all()
    serializer_class = MakeUpPostSerializer
    permission_classes = [IsAuthenticated, ArrivalPermission]


@extend_schema(tags=['MakeUp'])
@extend_schema_view(
    get=extend_schema(
        summary='Get a makeup',
        description='Get a makeup',
    ),
    put=extend_schema(
        summary='Update a makeup',
        description='Update a makeup',
    ),
    patch=extend_schema(
        summary='Update a makeup',
        description='Update a makeup',
    ),
    delete=extend_schema(
        summary='Delete a makeup',
        description='Delete a makeup',
    ),
)
class MakeUpRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a makeup.
    """
    queryset = MakeUp.objects.all()
    serializer_class = MakeUpGetSerializer
    permission_classes = [IsAuthenticated, ArrivalPermission]
