from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from django.db.models import F, OuterRef, Subquery, Sum, IntegerField
from django.db.models.functions import Coalesce
from rest_framework.response import Response


from apps.sez.models import ClearedItem
from apps.declaration.models import DeclaredItem
from apps.sez.serializers.available_declaration import AvailableDeclarationSerializer
from apps.sez.permissions import STZPermission


@extend_schema(tags=['Sez'])
@extend_schema_view(
    get=extend_schema(
        summary='Get available declarations for customs clearance',
        description='Permission: admin, stz_reader',
    ),
)
class GetAvailableDeclarationsView(APIView):
    """
    Get available declarations for customs clearance
    """
    permission_classes = (IsAuthenticated, STZPermission)
    serializer_class = AvailableDeclarationSerializer

    def get(self, request):
        """
SELECT  declaration_declaration.id,
declaration_declaration.declaration_number,
declaration_declareditem.ordinal_number,
declaration_declareditem.quantity - (
    select SUM(sez_cleareditem.quantity) from sez_cleareditem
    where declaration_declareditem.id = sez_cleareditem.declared_item_id_id
    ) as real_amount,
declaration_declareditem.quantity,declaration_declareditem.unit_name,
declaration_declareditem.name
  FROM [bloomtest].[dbo].[declaration_declaration]
  join declaration_declareditem on declaration_declaration.id = declaration_declareditem.declaration_id
  --left join sez_cleareditem on declaration_declareditem.id = sez_cleareditem.declared_item_id_id
  where declaration_declareditem.quantity  - (
      select SUM(sez_cleareditem.quantity) from sez_cleareditem
      where declaration_declareditem.id = sez_cleareditem.declared_item_id_id) > 0
        """
        cleared_items_subquery = ClearedItem.objects.filter(
            declared_item_id=OuterRef('id')
        ).values('declared_item_id').annotate(
            total_cleared=Sum('quantity', output_field=IntegerField())
        ).values('total_cleared').order_by()

        queryset = DeclaredItem.objects.annotate(
            real_amount=F('quantity') - Coalesce(Subquery(cleared_items_subquery), 0)
        ).filter(
            real_amount__gt=0
        ).values(
            'declaration__id',
            'declaration__declaration_number',
            'id',
            'ordinal_number',
            'real_amount',
            'quantity',
            'unit_name',
            'name'
        )

        data = list(queryset)
        result = list()
        for item in data:
            decl = {
                'declaration__id': item['declaration__id'],
                'declaration__declaration_number': item['declaration__declaration_number'],
                'items': list()
                }
            for i in result:
                if i['declaration__id'] == item['declaration__id']:
                    i['items'].append(item)
                    break
            else:
                decl['items'].append(item)
                result.append(decl)

        serializer = AvailableDeclarationSerializer(result, many=True)
        return Response(serializer.data)
