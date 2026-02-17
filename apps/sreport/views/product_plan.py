from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.sreport.models import ProductPlan
from apps.sreport.serializers.pruduct_plan import ProductPlanGetSerializer, ProductPlanPostSerializer


@extend_schema(tags=['ProductPlan'])
@extend_schema_view(
    get=extend_schema(
        summary='Get list product plans',
        description='Permission: AllowAny',
    ),
)
class ProductPlanListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductPlanGetSerializer
    queryset = ProductPlan.objects.all()


@extend_schema(tags=['ProductPlan'])
@extend_schema_view(
    post=extend_schema(
        summary='Create a product plan',
        description='Permission: IsAuthenticated',
    ),
)
class ProductPlanCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProductPlanPostSerializer
    queryset = ProductPlan.objects.all()


@extend_schema(tags=['ProductPlan'])
@extend_schema_view(
    get=extend_schema(
        summary='Get, update or delete a product plan',
        description='Permission: IsAuthenticated',
    ),
    put=extend_schema(
        summary='Update a product plan',
        description='Permission: IsAuthenticated',
    ),
    patch=extend_schema(
        summary='Partial update a product plan',
        description='Permission: IsAuthenticated',
    ),
    delete=extend_schema(
        summary='Delete a product plan',
        description='Permission: IsAuthenticated',
    ),
)
class ProductPlanUpdateView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProductPlanPostSerializer
    queryset = ProductPlan.objects.all()
