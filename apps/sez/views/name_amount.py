from drf_spectacular.utils import extend_schema, extend_schema_view
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
    ),
)
class NameAmountView(ListAPIView):
    permission_classes = (IsAuthenticated, STZPermission)
    serializer_class = NameAmountSerializer
    queryset = Models.objects.all()

    def get(self, request):
        """
SELECT [models].[id], [model_names].[short_name], [models].[code], COUNT_BIG([products].[id]) AS [real_amount]
FROM [models]
INNER JOIN [products] ON ([models].[id] = [products].[model_id])
INNER JOIN [model_names] ON ([models].[name_id] = [model_names].[id])
WHERE (([products].[cleared] IS NULL OR [products].[cleared] = 0) AND [products].[id] IS NOT NULL)
GROUP BY [models].[id], [model_names].[short_name], [models].[code] ORDER BY [model_names].[short_name]
        """
        queryset = Models.objects.filter(
            Q(products__cleared__isnull=True) | Q(products__cleared=0),
            products__isnull=False
        ).values('id', 'name__short_name', 'code').annotate(
            real_amount=Count('products')
        ).order_by('name__short_name')

        serializer = NameAmountSerializer(queryset, many=True)
        return Response(serializer.data)
