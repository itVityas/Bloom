from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter)
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from rest_framework.response import Response

from apps.sez.permissions import STZPermission
from apps.sez.serializers.name_amount import NameAmountSerializer
from apps.shtrih.models import Models


@extend_schema(tags=['Sez'])
@extend_schema_view(
    get=extend_schema(
        summary='Get short name code and real_amount',
        description='Permission: admin, stz_reader, stz',
        parameters=[
            OpenApiParameter(
                name='ziro',
                type=bool,
                location=OpenApiParameter.HEADER,
                required=False,
                description='if ziro having count(products.id)=0 else >0'
            ),
        ],
    ),
)
class NameAmountView(ListAPIView):
    permission_classes = (IsAuthenticated, STZPermission)
    serializer_class = NameAmountSerializer
    queryset = Models.objects.all()

    def get(self, request):
        """
SELECT
[models].[name_id], [model_names].[short_name], [models].[code], COUNT_BIG([products].[id]) AS [real_amount]
FROM [models]
LEFT OUTER JOIN [products] ON ([models].[id] = [products].[model_id])
INNER JOIN [model_names] ON ([models].[name_id] = [model_names].[id])
WHERE ([products].[cleared] IS NULL OR [products].[cleared] = 0)
GROUP BY [models].[name_id], [model_names].[short_name], [models].[code]
HAVING COUNT_BIG([products].[id]) = 0
ORDER BY [model_names].[short_name] ASC OFFSET 0 ROWS
        """
        ziro = request.query_params.get('ziro', False)
        if ziro:
            queryset = Models.objects.filter(
                Q(products__cleared__isnull=True) | Q(products__cleared=0)
            ).values('name__id', 'name__short_name', 'code').annotate(
                real_amount=Count('products')
            ).filter(real_amount=0).order_by('name__short_name')
        else:
            queryset = Models.objects.filter(
                Q(products__cleared__isnull=True) | Q(products__cleared=0)
            ).values('name__id', 'name__short_name', 'code').annotate(
                real_amount=Count('products')
            ).filter(real_amount__gt=0).order_by('name__short_name')

        serializer = NameAmountSerializer(queryset, many=True)
        return Response(serializer.data)
