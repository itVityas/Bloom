from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.general.models import AddTitle
from apps.general.serializers.add_title import AddTitleSerializer, AddTitleGetSerializer
from apps.general.permission import AddPermission


@extend_schema(tags=['AddTitle'])
@extend_schema_view(
    post=extend_schema(
        summary='Create AddTitle',
        description='Permission: Admin, Add',
    )
)
class AddTitleCreateAPIView(CreateAPIView):
    queryset = AddTitle.objects.all()
    serializer_class = AddTitleSerializer
    permission_classes = (IsAuthenticated, AddPermission)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)


@extend_schema(tags=['AddTitle'])
@extend_schema_view(
    get=extend_schema(
        summary='Get list of AddTitle',
        description='Permission: User',
    ),
)
class AddTitleListAPIView(ListAPIView):
    queryset = AddTitle.objects.all()
    serializer_class = AddTitleGetSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)


@extend_schema(tags=['AddTitle'])
@extend_schema_view(
    get=extend_schema(
        summary='Get AddTitle',
        description='Permission: User',
    ),
    put=extend_schema(
        summary='Update AddTitle',
        description='Permission: Admin, Add',
    ),
    patch=extend_schema(
        summary='Update AddTitle',
        description='Permission: Admin, Add',
    ),
    delete=extend_schema(
        summary='Delete AddTitle',
        description='Permission: Admin, Add',
    )
)
class AddTitleRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = AddTitle.objects.all()
    serializer_class = AddTitleSerializer
    permission_classes = (IsAuthenticated, AddPermission)
