from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response

from apps.shtrih.models import ModelNames
from apps.shtrih.serializers.model_name import ModelNamesSerializer
from apps.shtrih.permission import StrihPermission
from Bloom.paginator import StandartResultPaginator


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='Get list Model',
        description="description='Permission: admin, strih"
    )
)
class ModelNameListView(ListAPIView):
    queryset = ModelNames.objects.all()
    serializer_class = ModelNamesSerializer
    permission_classes = (IsAuthenticated, StrihPermission)
    pagination_class = StandartResultPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'name', 'short_name')


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='Get list Model by product_code',
        description="description='Permission: admin, strih",
        parameters=[
            OpenApiParameter(
                name='production_code_id',
                location=OpenApiParameter.QUERY,
                description='production_code.id',
                required=True,
                type=int,
            ),
        ],
    )
)
class ModelNameByProductCodeListView(ListAPIView):
    queryset = ModelNames.objects.all()
    serializer_class = ModelNamesSerializer
    permission_classes = (IsAuthenticated, StrihPermission)
    pagination_class = StandartResultPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'name', 'short_name')

    def get(self, request):
        production_code_id = request.query_params.get('production_code_id', None)
        if not production_code_id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'product_code not fount'}
            )
        queryset = ModelNames.objects.filter(models__production_code=production_code_id)
        page = self.paginate_queryset(queryset)
        serializer = ModelNamesSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
