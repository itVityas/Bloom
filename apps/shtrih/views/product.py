from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend

from apps.shtrih.models import Products
from apps.shtrih.serializers.products import ProductGetSerializer
from apps.shtrih.permission import StrihPermission


@extend_schema(tags=['Shtrih'])
@extend_schema_view(
    get=extend_schema(
        summary='List of Products',
        description="description='Permission: admin, strih",
    )
)
class ProductListView(ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductGetSerializer
    permission_classes = (IsAuthenticated, StrihPermission)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id',
        'barcode',
        'state',
        'nameplate',
        'quantity',
        'cleared'
        ]
