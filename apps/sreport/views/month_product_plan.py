from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.sreport.models import MonthProductPlan
from apps.sreport.serializers.month_product_plan import MonthProductPlanSerializer


@extend_schema(tags=['ProductPlan'])
@extend_schema_view(
    get=extend_schema(
        summary='Get list month product plans',
        description='Permission: AllowAny',
    ),
    post=extend_schema(
        summary='Create a month product plan',
        description='Permission: AllowAny',
    ),
)
class MonthProductPlanListView(ListCreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = MonthProductPlanSerializer
    queryset = MonthProductPlan.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['month', 'year']


@extend_schema(tags=['ProductPlan'])
@extend_schema_view(
    get=extend_schema(
        summary='Get a month product plan',
        description='Permission: AllowAny',
    ),
    put=extend_schema(
        summary='Update a month product plan',
        description='Permission: AllowAny',
    ),
    patch=extend_schema(
        summary='Partial update a month product plan',
        description='Permission: AllowAny',
    ),
    delete=extend_schema(
        summary='Delete a month product plan',
        description='Permission: AllowAny',
    )
)
class MonthProductPlanDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = MonthProductPlanSerializer
    queryset = MonthProductPlan.objects.all()
