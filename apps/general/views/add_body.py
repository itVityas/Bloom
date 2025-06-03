from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.general.models import AddBody
from apps.general.serializers.add_body import AddBodySerializer
from apps.general.permission import AddPermission


@extend_schema(tags=['AddBody'])
@extend_schema_view(
    get=extend_schema(
        summary='List AddBody',
        description='Permission: User',
    ),
    post=extend_schema(
        summary='Create AddBody',
        description='Permission: Admin, Add',
    ),
)
class AddBodyListCreateAPIView(ListCreateAPIView):
    """
    API endpoint that allows AddBody entries to be listed or created.
    """
    queryset = AddBody.objects.all()
    serializer_class = AddBodySerializer
    permission_classes = (IsAuthenticated, AddPermission)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('body', 'title',)


@extend_schema(tags=['AddBody'])
@extend_schema_view(
    get=extend_schema(
        summary='Retrieve AddBody',
        description='Permission: User',
    ),
    put=extend_schema(
        summary='Update AddBody',
        description='Permission: Admin, Add',
    ),
    patch=extend_schema(
        summary='Partial Update AddBody',
        description='Permission: Admin, Add',
    ),
    delete=extend_schema(
        summary='Delete AddBody',
        description='Permission: Admin, Add',
    ),
)
class AddBodyRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows single AddBody entry to be retrieved, updated or deleted.
    """
    queryset = AddBody.objects.all()
    serializer_class = AddBodySerializer
    permission_classes = (IsAuthenticated, AddPermission)
