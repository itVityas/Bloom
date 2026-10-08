from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.sreport.models import YearProductPlan
from apps.sreport.serializers.year_product_plan import YearProductPlanSerializer
from apps.sreport.permission import ProductPlanPermission


@extend_schema(tags=['ProductPlan'])
@extend_schema_view(
    get=extend_schema(
        summary='Get list year product plans',
        description='Permission: AllowAny',
    ),
    post=extend_schema(
        summary='Create a year product plan',
        description='Permission: AllowAny',
    ),
)
class YearProductPlanListView(ListCreateAPIView):
    permission_classes = [AllowAny, ProductPlanPermission]
    serializer_class = YearProductPlanSerializer
    queryset = YearProductPlan.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['year']


@extend_schema(tags=['ProductPlan'])
@extend_schema_view(
    get=extend_schema(
        summary='Get a year product plan',
        description='Permission: AllowAny',
    ),
    put=extend_schema(
        summary='Update a year product plan',
        description='Permission: AllowAny',
    ),
    patch=extend_schema(
        summary='Partial update a year product plan',
        description='Permission: AllowAny',
    ),
    delete=extend_schema(
        summary='Delete a year product plan',
        description='Permission: AllowAny',
    )
)
class YearProductPlanDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny, ProductPlanPermission]
    serializer_class = YearProductPlanSerializer
    queryset = YearProductPlan.objects.all()
